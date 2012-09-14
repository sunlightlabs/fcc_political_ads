# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AddressLabel.created_by'
        db.add_column('locations_addresslabel', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations_addresslabel_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'AddressLabel.updated_by'
        db.add_column('locations_addresslabel', 'updated_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations_addresslabel_updated', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'AddressLabel.approved_by'
        db.add_column('locations_addresslabel', 'approved_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations_addresslabel_approved', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'AddressLabel.created_at'
        db.add_column('locations_addresslabel', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 9, 17, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'AddressLabel.updated_at'
        db.add_column('locations_addresslabel', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AddressLabel.approved_at'
        db.add_column('locations_addresslabel', 'approved_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AddressLabel.notes'
        db.add_column('locations_addresslabel', 'notes',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Address.created_by'
        db.add_column('locations_address', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations_address_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Address.updated_by'
        db.add_column('locations_address', 'updated_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations_address_updated', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Address.approved_by'
        db.add_column('locations_address', 'approved_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations_address_approved', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Address.created_at'
        db.add_column('locations_address', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 9, 17, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Address.updated_at'
        db.add_column('locations_address', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Address.approved_at'
        db.add_column('locations_address', 'approved_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Address.notes'
        db.add_column('locations_address', 'notes',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AddressLabel.created_by'
        db.delete_column('locations_addresslabel', 'created_by_id')

        # Deleting field 'AddressLabel.updated_by'
        db.delete_column('locations_addresslabel', 'updated_by_id')

        # Deleting field 'AddressLabel.approved_by'
        db.delete_column('locations_addresslabel', 'approved_by_id')

        # Deleting field 'AddressLabel.created_at'
        db.delete_column('locations_addresslabel', 'created_at')

        # Deleting field 'AddressLabel.updated_at'
        db.delete_column('locations_addresslabel', 'updated_at')

        # Deleting field 'AddressLabel.approved_at'
        db.delete_column('locations_addresslabel', 'approved_at')

        # Deleting field 'AddressLabel.notes'
        db.delete_column('locations_addresslabel', 'notes')

        # Deleting field 'Address.created_by'
        db.delete_column('locations_address', 'created_by_id')

        # Deleting field 'Address.updated_by'
        db.delete_column('locations_address', 'updated_by_id')

        # Deleting field 'Address.approved_by'
        db.delete_column('locations_address', 'approved_by_id')

        # Deleting field 'Address.created_at'
        db.delete_column('locations_address', 'created_at')

        # Deleting field 'Address.updated_at'
        db.delete_column('locations_address', 'updated_at')

        # Deleting field 'Address.approved_at'
        db.delete_column('locations_address', 'approved_at')

        # Deleting field 'Address.notes'
        db.delete_column('locations_address', 'notes')


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
        'locations.address': {
            'Meta': {'unique_together': "(('address1', 'address2', 'city', 'state', 'zipcode'),)", 'object_name': 'Address'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations_address_approved'", 'null': 'True', 'to': "orm['auth.User']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations_address_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations_address_updated'", 'null': 'True', 'to': "orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'locations.addresslabel': {
            'Meta': {'object_name': 'AddressLabel'},
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations_addresslabel_approved'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations_addresslabel_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations_addresslabel_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['locations']