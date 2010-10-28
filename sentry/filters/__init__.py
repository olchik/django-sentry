# Widget api is pretty ugly
from django.conf import settings
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.db.models import Q

from sentry import conf

class Widget(object):
    def __init__(self, filter, request):
        self.filter = filter
        self.request = request

    def get_query_string(self):
        return self.filter.get_query_string()

class TextWidget(Widget):
    def render(self, value):
        return mark_safe('<div id="search"><p class="textfield"><input type="text" name="%(name)s" value="%(value)s"/></p><p class="submit"><input type="submit" class="search-submit"/></p></div>' % dict(
            name=self.filter.get_query_param(),
            value=value,
        ))

class ChoiceWidget(Widget):
    def render(self, value):
        choices = self.filter.get_choices()
        query_string = self.get_query_string()
        column = self.filter.get_query_param()

        output = ['<ul class="%s-list filter-list sidebar-module">' % (self.filter.column,)]
        output.append('<li%(active)s><a href="%(query_string)s&amp;%(column)s">Any %(label)s</a></li>' % dict(
            active=not value and ' class="active"' or '',
            query_string=query_string,
            label=self.filter.label,
            column=column,
        ))
        for key, val in choices.iteritems():
            key = unicode(key)
            output.append('<li%(active)s><a href="%(query_string)s&amp;%(column)s=%(key)s">%(value)s</a></li>' % dict(
                active=value == key and ' class="active"' or '',
                column=column,
                key=key,
                value=val,
                query_string=query_string,
            ))
        output.append('</ul>')
        return mark_safe('\n'.join(output))

class SentryFilter(object):
    label = ''
    column = ''
    widget = ChoiceWidget
    # This must be a string
    default = ''
    message_type = conf.ANY

    @property
    def message_type_title(self):
        for msg_type, label in conf.MESSAGE_TYPES:
            if msg_type == self.message_type:
                return label

    def __init__(self, request):
        self.request = request
    
    def is_set(self):
        return bool(self.get_value())
    
    def get_value(self):
        return self.request.GET.get(self.get_query_param(), self.default) or ''
    
    def get_query_param(self):
        return getattr(self, 'query_param', self.column)

    def get_widget(self):
        return self.widget(self, self.request)
    
    def get_query_string(self):
        column = self.column
        query_dict = self.request.GET.copy()
        if 'p' in query_dict:
            del query_dict['p']
        if column in query_dict:
            del query_dict[self.column]
        return '?' + query_dict.urlencode()
    
    def get_choices(self):
        from sentry.models import FilterValue
        return SortedDict((l, l) for l in FilterValue.objects.filter(key=self.column)\
                                                     .values_list('value', flat=True)\
                                                     .order_by('value'))

    def _get_query(self):
        try:
            from indexer.models import Index
            kwargs = {self.column: self.get_value()}
    #        if self.column.startswith('data__'):
    #            return Index.objects.get_for_queryset(queryset, **kwargs)
            return  Q(**kwargs) |self._get_other_query()
        except Exception, ex:
            print ex

    def _get_other_query(self):
        if not self.message_type is None:
            return ~Q(message_type=self.message_type)
        else:
            return Q()
    
    def process(self, data):
        """``self.request`` is not available within this method"""
        return data
    
    def render(self):
        widget = self.get_widget()
        return widget.render(self.get_value())


class MessageTypeFilter(SentryFilter):
    label = 'Message Type'
    column = 'message_type'
    default = None

    def get_choices(self):
        return SortedDict(conf.MESSAGE_TYPES)


class StatusFilter(SentryFilter):
    label = 'Status'
    column = 'status'
    default = None

    def get_choices(self):
        return SortedDict([
            (0, 'Unresolved'),
            (1, 'Resolved'),
        ])


class TestResultsFilter(SentryFilter):
    label = 'Test Result'
    column = 'test_result'
    message_type = conf.TEST

    def get_choices(self):
        from sentry.models import TEST_RESULTS
        return SortedDict(TEST_RESULTS)

class LoggerFilter(SentryFilter):
    label = 'Logger'
    column = 'logger'
    message_type = conf.LOG

class ServerNameFilter(SentryFilter):
    label = 'Server Name'
    column = 'server_name'

    def _get_query(self):
        return Q(message_set__server_name=self.get_value())

class SiteFilter(SentryFilter):
    label = 'Site'
    column = 'site'

    def process(self, data):
        if 'site' in data:
            return data
        if conf.SITE is None:
            if 'django.contrib.sites' in settings.INSTALLED_APPS:
                from odash.main.models import Site
                try:
                    conf.SITE = Site.objects.get_current().name
                except:
                    conf.SITE = ''
            else:
                conf.SITE = ''
        if conf.SITE:
            data['site'] = conf.SITE
        return data

    def _get_query(self):
        return Q(message_set__site=self.get_value())

class LevelFilter(SentryFilter):
    label = 'Level'
    column = 'level'
    message_type = conf.LOG

    def get_choices(self):
        return SortedDict((str(k), v) for k, v in conf.LOG_LEVELS)