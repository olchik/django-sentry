# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GroupedMessage'
        db.create_table('sentry_groupedmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('message_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Project'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('traceback', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('logger', self.gf('django.db.models.fields.CharField')(default='root', max_length=64, db_index=True, blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(default=40, db_index=True, blank=True)),
            ('test_result', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.Test'], null=True, blank=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('times_seen', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('first_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
        ))
        db.send_create_signal('sentry', ['GroupedMessage'])

        # Adding unique constraint on 'GroupedMessage', fields ['message_type', 'name', 'checksum', 'project']
        db.create_unique('sentry_groupedmessage', ['message_type', 'name', 'checksum', 'project_id'])

        # Adding model 'Message'
        db.create_table('sentry_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('message_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Project'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('traceback', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('logger', self.gf('django.db.models.fields.CharField')(default='root', max_length=64, db_index=True, blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(default=40, db_index=True, blank=True)),
            ('test_result', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.Test'], null=True, blank=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='message_set', null=True, to=orm['sentry.GroupedMessage'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Site'], null=True)),
        ))
        db.send_create_signal('sentry', ['Message'])

        # Adding model 'FilterValue'
        db.create_table('sentry_filtervalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('sentry', ['FilterValue'])

        # Adding unique constraint on 'FilterValue', fields ['key', 'value']
        db.create_unique('sentry_filtervalue', ['key', 'value'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FilterValue', fields ['key', 'value']
        db.delete_unique('sentry_filtervalue', ['key', 'value'])

        # Removing unique constraint on 'GroupedMessage', fields ['message_type', 'name', 'checksum', 'project']
        db.delete_unique('sentry_groupedmessage', ['message_type', 'name', 'checksum', 'project_id'])

        # Deleting model 'GroupedMessage'
        db.delete_table('sentry_groupedmessage')

        # Deleting model 'Message'
        db.delete_table('sentry_message')

        # Deleting model 'FilterValue'
        db.delete_table('sentry_filtervalue')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'main.site': {
            'Meta': {'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sites'", 'null': 'True', 'to': "orm['main.Project']"}),
            'servername': ('django.db.models.fields.CharField', [], {'default': "'example.com'", 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'sentry.filtervalue': {
            'Meta': {'unique_together': "(('key', 'value'),)", 'object_name': 'FilterValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sentry.groupedmessage': {
            'Meta': {'unique_together': "(('message_type', 'name', 'checksum', 'project'),)", 'object_name': 'GroupedMessage'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'class_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '40', 'db_index': 'True', 'blank': 'True'}),
            'logger': ('django.db.models.fields.CharField', [], {'default': "'root'", 'max_length': '64', 'db_index': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'message_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Project']"}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.Test']", 'null': 'True', 'blank': 'True'}),
            'test_result': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'times_seen': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'traceback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'sentry.message': {
            'Meta': {'object_name': 'Message'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'class_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'message_set'", 'null': 'True', 'to': "orm['sentry.GroupedMessage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '40', 'db_index': 'True', 'blank': 'True'}),
            'logger': ('django.db.models.fields.CharField', [], {'default': "'root'", 'max_length': '64', 'db_index': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'message_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Project']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Site']", 'null': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.Test']", 'null': 'True', 'blank': 'True'}),
            'test_result': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'traceback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'testing.test': {
            'Meta': {'object_name': 'Test'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order_in_dashboard': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tests'", 'null': 'True', 'to': "orm['main.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['sentry']
