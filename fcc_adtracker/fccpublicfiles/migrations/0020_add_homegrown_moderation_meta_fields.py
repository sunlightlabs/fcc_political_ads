# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from uuid import UUID


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PoliticalBuy.created_by'
        db.add_column('fccpublicfiles_politicalbuy', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_politicalbuy_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PoliticalBuy.updated_by'
        db.add_column('fccpublicfiles_politicalbuy', 'updated_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_politicalbuy_updated', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PoliticalBuy.approved_by'
        db.add_column('fccpublicfiles_politicalbuy', 'approved_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_politicalbuy_approved', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PoliticalBuy.approved_at'
        db.add_column('fccpublicfiles_politicalbuy', 'approved_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        db.rename_column('fccpublicfiles_politicalbuy', 'is_visible', 'is_public')

        # Adding field 'PoliticalBuy.notes'
        db.add_column('fccpublicfiles_politicalbuy', 'notes',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Organization.created_by'
        db.add_column('fccpublicfiles_organization', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_organization_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Organization.updated_by'
        db.add_column('fccpublicfiles_organization', 'updated_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_organization_updated', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Organization.approved_by'
        db.add_column('fccpublicfiles_organization', 'approved_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_organization_approved', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Organization.created_at'
        db.add_column('fccpublicfiles_organization', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 9, 14, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Organization.updated_at'
        db.add_column('fccpublicfiles_organization', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Organization.approved_at'
        db.add_column('fccpublicfiles_organization', 'approved_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        db.rename_column('fccpublicfiles_organization', 'is_visible', 'is_public')

        # Adding field 'Organization.notes'
        db.add_column('fccpublicfiles_organization', 'notes',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PoliticalSpot.created_by'
        db.add_column('fccpublicfiles_politicalspot', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_politicalspot_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PoliticalSpot.updated_by'
        db.add_column('fccpublicfiles_politicalspot', 'updated_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_politicalspot_updated', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PoliticalSpot.approved_by'
        db.add_column('fccpublicfiles_politicalspot', 'approved_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_politicalspot_approved', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PoliticalSpot.approved_at'
        db.add_column('fccpublicfiles_politicalspot', 'approved_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        db.rename_column('fccpublicfiles_politicalspot', 'is_visible', 'is_public')

        # Adding field 'PoliticalSpot.notes'
        db.add_column('fccpublicfiles_politicalspot', 'notes',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Role.created_by'
        db.add_column('fccpublicfiles_role', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_role_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Role.updated_by'
        db.add_column('fccpublicfiles_role', 'updated_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_role_updated', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Role.approved_by'
        db.add_column('fccpublicfiles_role', 'approved_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_role_approved', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Role.created_at'
        db.add_column('fccpublicfiles_role', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 9, 14, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Role.updated_at'
        db.add_column('fccpublicfiles_role', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Role.approved_at'
        db.add_column('fccpublicfiles_role', 'approved_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        db.rename_column('fccpublicfiles_role', 'is_visible', 'is_public')

        # Adding field 'Role.notes'
        db.add_column('fccpublicfiles_role', 'notes',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.created_by'
        db.add_column('fccpublicfiles_person', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_person_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Person.updated_by'
        db.add_column('fccpublicfiles_person', 'updated_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_person_updated', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Person.approved_by'
        db.add_column('fccpublicfiles_person', 'approved_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fccpublicfiles_person_approved', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Person.created_at'
        db.add_column('fccpublicfiles_person', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 9, 14, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Person.updated_at'
        db.add_column('fccpublicfiles_person', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.approved_at'
        db.add_column('fccpublicfiles_person', 'approved_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        db.rename_column('fccpublicfiles_person', 'is_visible', 'is_public')

        # Adding field 'Person.notes'
        db.add_column('fccpublicfiles_person', 'notes',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PoliticalBuy.created_by'
        db.delete_column('fccpublicfiles_politicalbuy', 'created_by_id')

        # Deleting field 'PoliticalBuy.updated_by'
        db.delete_column('fccpublicfiles_politicalbuy', 'updated_by_id')

        # Deleting field 'PoliticalBuy.approved_by'
        db.delete_column('fccpublicfiles_politicalbuy', 'approved_by_id')

        # Deleting field 'PoliticalBuy.approved_at'
        db.delete_column('fccpublicfiles_politicalbuy', 'approved_at')

        db.rename_column('fccpublicfiles_politicalbuy', 'is_public', 'is_visible')

        # Deleting field 'PoliticalBuy.notes'
        db.delete_column('fccpublicfiles_politicalbuy', 'notes')

        # Deleting field 'Organization.created_by'
        db.delete_column('fccpublicfiles_organization', 'created_by_id')

        # Deleting field 'Organization.updated_by'
        db.delete_column('fccpublicfiles_organization', 'updated_by_id')

        # Deleting field 'Organization.approved_by'
        db.delete_column('fccpublicfiles_organization', 'approved_by_id')

        # Deleting field 'Organization.created_at'
        db.delete_column('fccpublicfiles_organization', 'created_at')

        # Deleting field 'Organization.updated_at'
        db.delete_column('fccpublicfiles_organization', 'updated_at')

        # Deleting field 'Organization.approved_at'
        db.delete_column('fccpublicfiles_organization', 'approved_at')

        db.rename_column('fccpublicfiles_organization', 'is_public', 'is_visible')

        # Deleting field 'Organization.notes'
        db.delete_column('fccpublicfiles_organization', 'notes')

        # Deleting field 'PoliticalSpot.created_by'
        db.delete_column('fccpublicfiles_politicalspot', 'created_by_id')

        # Deleting field 'PoliticalSpot.updated_by'
        db.delete_column('fccpublicfiles_politicalspot', 'updated_by_id')

        # Deleting field 'PoliticalSpot.approved_by'
        db.delete_column('fccpublicfiles_politicalspot', 'approved_by_id')

        # Deleting field 'PoliticalSpot.approved_at'
        db.delete_column('fccpublicfiles_politicalspot', 'approved_at')

        db.rename_column('fccpublicfiles_politicalspot', 'is_public', 'is_visible')

        # Deleting field 'PoliticalSpot.notes'
        db.delete_column('fccpublicfiles_politicalspot', 'notes')

        # Deleting field 'Role.created_by'
        db.delete_column('fccpublicfiles_role', 'created_by_id')

        # Deleting field 'Role.updated_by'
        db.delete_column('fccpublicfiles_role', 'updated_by_id')

        # Deleting field 'Role.approved_by'
        db.delete_column('fccpublicfiles_role', 'approved_by_id')

        # Deleting field 'Role.created_at'
        db.delete_column('fccpublicfiles_role', 'created_at')

        # Deleting field 'Role.updated_at'
        db.delete_column('fccpublicfiles_role', 'updated_at')

        # Deleting field 'Role.approved_at'
        db.delete_column('fccpublicfiles_role', 'approved_at')

        db.rename_column('fccpublicfiles_role', 'is_public', 'is_visible')

        # Deleting field 'Role.notes'
        db.delete_column('fccpublicfiles_role', 'notes')

        # Deleting field 'Person.created_by'
        db.delete_column('fccpublicfiles_person', 'created_by_id')

        # Deleting field 'Person.updated_by'
        db.delete_column('fccpublicfiles_person', 'updated_by_id')

        # Deleting field 'Person.approved_by'
        db.delete_column('fccpublicfiles_person', 'approved_by_id')

        # Deleting field 'Person.created_at'
        db.delete_column('fccpublicfiles_person', 'created_at')

        # Deleting field 'Person.updated_at'
        db.delete_column('fccpublicfiles_person', 'updated_at')

        # Deleting field 'Person.approved_at'
        db.delete_column('fccpublicfiles_person', 'approved_at')

        db.rename_column('fccpublicfiles_person', 'is_public', 'is_visible')

        # Deleting field 'Person.notes'
        db.delete_column('fccpublicfiles_person', 'notes')


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
        'broadcasters.broadcaster': {
            'Meta': {'ordering': "('community_state', 'community_city', 'callsign')", 'object_name': 'Broadcaster'},
            'callsign': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'channel': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'community_city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'community_state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'dma_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facility_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facility_type': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network_affiliate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nielsen_dma': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
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
            'access_level': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '32'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'}),
            'dc_properties': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doccloud.DocumentCloudProperties']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "('title',)", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'doccloud.documentcloudproperties': {
            'Meta': {'object_name': 'DocumentCloudProperties'},
            'dc_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'dc_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'fccpublicfiles.genericpublicdocument': {
            'Meta': {'object_name': 'GenericPublicDocument'},
            'broadcasters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['broadcasters.Broadcaster']", 'null': 'True', 'symmetrical': 'False'}),
            'documentcloud_doc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doccloud.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'fccpublicfiles.organization': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organization'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['locations.Address']", 'null': 'True', 'blank': 'True'}),
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_organization_approved'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_organization_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'employees': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fccpublicfiles.Person']", 'through': "orm['fccpublicfiles.Role']", 'symmetrical': 'False'}),
            'fec_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_organization_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'fccpublicfiles.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person'},
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_person_approved'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_person_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_person_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'fccpublicfiles.politicalbuy': {
            'Meta': {'object_name': 'PoliticalBuy'},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'advertiser_politicalbuys'", 'null': 'True', 'to': "orm['fccpublicfiles.Organization']"}),
            'advertiser_signatory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Person']", 'null': 'True', 'blank': 'True'}),
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_politicalbuy_approved'", 'null': 'True', 'to': "orm['auth.User']"}),
            'bought_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mediabuyer_politicalbuys'", 'null': 'True', 'to': "orm['fccpublicfiles.Organization']"}),
            'broadcasters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['broadcasters.Broadcaster']", 'null': 'True', 'symmetrical': 'False'}),
            'contract_end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True', 'blank': 'True'}),
            'contract_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'contract_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_politicalbuy_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'documentcloud_doc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doccloud.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lowest_unit_price': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'num_spots_raw': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'total_spent_raw': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_politicalbuy_updated'", 'null': 'True', 'to': "orm['auth.User']"}),
            'uuid_key': ('django.db.models.fields.CharField', [], {'default': "UUID('e7dc7310-dcd1-428a-8a33-a3aadeb6e3be')", 'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        'fccpublicfiles.politicalspot': {
            'Meta': {'object_name': 'PoliticalSpot'},
            'airing_days': ('weekday_field.fields.WeekdayField', [], {'max_length': '14', 'blank': 'True'}),
            'airing_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'airing_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_politicalspot_approved'", 'null': 'True', 'to': "orm['auth.User']"}),
            'broadcast_length': ('timedelta.fields.TimedeltaField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_politicalspot_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.PoliticalBuy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'num_spots': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preemptable': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'show_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'timeslot_begin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'timeslot_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_politicalspot_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'fccpublicfiles.role': {
            'Meta': {'object_name': 'Role'},
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_role_approved'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_role_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fccpublicfiles_role_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'locations.address': {
            'Meta': {'unique_together': "(('address1', 'address2', 'city', 'state', 'zipcode'),)", 'object_name': 'Address'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['fccpublicfiles']
