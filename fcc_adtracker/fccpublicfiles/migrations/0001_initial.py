# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PublicDocument'
        db.create_table('fccpublicfiles_publicdocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('station', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('documentcloud_doc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doccloud.Document'])),
        ))
        db.send_create_signal('fccpublicfiles', ['PublicDocument'])

        # Adding model 'PoliticalDocument'
        db.create_table('fccpublicfiles_politicaldocument', (
            ('publicdocument_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fccpublicfiles.PublicDocument'], unique=True, primary_key=True)),
            ('contract_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('advertiser', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('ordered_by', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('contract_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 16, 0, 0), null=True, blank=True)),
            ('contract_end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 16, 0, 0), null=True, blank=True)),
        ))
        db.send_create_signal('fccpublicfiles', ['PoliticalDocument'])

        # Adding model 'PoliticalAd'
        db.create_table('fccpublicfiles_politicalad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fccpublicfiles.PoliticalDocument'])),
            ('airing_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 16, 0, 0), null=True, blank=True)),
            ('airing_end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 16, 0, 0), null=True, blank=True)),
            ('timeslot_begin', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('timeslot_end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('show_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('broadcast_length', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('num_spots', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('fccpublicfiles', ['PoliticalAd'])


    def backwards(self, orm):
        # Deleting model 'PublicDocument'
        db.delete_table('fccpublicfiles_publicdocument')

        # Deleting model 'PoliticalDocument'
        db.delete_table('fccpublicfiles_politicaldocument')

        # Deleting model 'PoliticalAd'
        db.delete_table('fccpublicfiles_politicalad')


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
        'doccloud.document': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Document'},
            'access_level': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'}),
            'dc_properties': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doccloud.DocumentCloudProperties']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "('title',)", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'doccloud.documentcloudproperties': {
            'Meta': {'object_name': 'DocumentCloudProperties'},
            'dc_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'dc_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'fccpublicfiles.politicalad': {
            'Meta': {'object_name': 'PoliticalAd'},
            'airing_end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 16, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'airing_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 16, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'broadcast_length': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.PoliticalDocument']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_spots': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'show_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timeslot_begin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'timeslot_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'fccpublicfiles.politicaldocument': {
            'Meta': {'object_name': 'PoliticalDocument', '_ormbases': ['fccpublicfiles.PublicDocument']},
            'advertiser': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contract_end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 16, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'contract_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contract_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 16, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'ordered_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'publicdocument_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fccpublicfiles.PublicDocument']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fccpublicfiles.publicdocument': {
            'Meta': {'object_name': 'PublicDocument'},
            'documentcloud_doc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doccloud.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'station': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['fccpublicfiles']