import datetime
import django
import logging
import warnings

from django.db import models
from django.db.models import signals

from sentry import conf
from sentry.helpers import construct_checksum

assert not conf.DATABASE_USING or django.VERSION >= (1, 2), 'The `SENTRY_DATABASE_USING` setting requires Django >= 1.2'

logger = logging.getLogger('sentry.errors')

class SentryManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        qs = super(SentryManager, self).get_query_set()
        if conf.DATABASE_USING:
            qs = qs.using(conf.DATABASE_USING)
        return qs

    def from_kwargs(self, **kwargs):
        from sentry.models import Message, GroupedMessage, FilterValue
        URL_MAX_LENGTH = Message._meta.get_field_by_name('url')[0].max_length

        name = kwargs.pop('name', None)
        message_type = kwargs.pop("message_type", conf.LOG)
        project = kwargs.pop("project")

        site = kwargs.pop('site', None)
        test_result = kwargs.pop('test_result', None)

        # Log specific
        logger_name = kwargs.pop('logger', '')
        url = kwargs.pop('url', None)
        data = kwargs.pop('data', {}) or {}
        if url:
            data['url'] = url
            url = url[:URL_MAX_LENGTH]

        checksum = construct_checksum(**kwargs)
        mail = False
        try:
            if 'url' in data:
                kwargs['data'] = {'url': data['url']}
            group, created = self._get_or_create_group_message(message_type, name,
                                                               checksum, project,
                                                               test_result, kwargs)
            kwargs.pop('data', None)
            if not created:
                self._update_counters(group)
            else: 
                mail = True

            instance = Message.objects.create(
                name=name,
                message_type=message_type,
                project=project,
                checksum=checksum,
                group=group,

                logger=logger_name,
                data=data,
                url=url,
                site=site,
                test_result=test_result,
                **kwargs
            )
            if site:
                print FilterValue.objects.all()
                
                FilterValue.objects.get_or_create(key='site__servername', value=site.servername, label=site.servername)
#            if site:
#                FilterValue.objects.get_or_create(key='site', value=site.id, label=site.name)
            if site:
                FilterValue.objects.get_or_create(key='project', value=project.id, label=project.name)
            if logger_name:
                FilterValue.objects.get_or_create(key='logger', value=logger_name, label=logger_name)
            if test_result:
                FilterValue.objects.get_or_create(key='test_result', value=test_result, label=test_result)
        except Exception, exc:
            # TODO: should we mail admins when there are failures?
            try:
                logger.exception(u'Unable to process log entry: %s' % (exc,))
            except Exception, exc:
                warnings.warn(u'Unable to process log entry: %s' % (exc,))
        else:
            if mail:
                group.mail_admins()
            return instance

    def _get_or_create_group_message(self, message_type, name, 
                                     checksum, project, test_result, kwargs):
        """
        In GroupedMessage unique together:
            name
            message_type
            checksum
            project
        Test nodes we also sort by test result.
        """
        from sentry.models import GroupedMessage
        params = dict(name=name,
                      project=project,
                      message_type=message_type,
                      checksum=checksum)
        if message_type == conf.TEST:
            params['test_result'] = test_result
        return GroupedMessage.objects.get_or_create(defaults=kwargs, **params)


    def _update_counters(self, group):
        from sentry.models import GroupedMessage
        now = datetime.datetime.now()
        GroupedMessage.objects.filter(pk=group.pk).update(
            times_seen=models.F('times_seen') + 1,
            status=0,
            last_seen=now,
        )
        # HACK: maintain appeared state
        if group.status == 1:
            mail = True
        group.status = 0
        group.last_seen = now
        group.times_seen += 1
        signals.post_save.send(sender=GroupedMessage, instance=group, created=False)


class GroupedMessageManager(SentryManager):
    def get_by_natural_key(self, logger, view, checksum):
        return self.get(logger=logger, view=view, checksum=checksum)