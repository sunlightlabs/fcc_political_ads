# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Address', fields ['address1', 'address2', 'state', 'zipcode', 'city']
        db.create_unique('fccpublicfiles_address', ['address1', 'address2', 'state', 'zipcode', 'city'])


    def backwards(self, orm):
        # Removing unique constraint on 'Address', fields ['address1', 'address2', 'state', 'zipcode', 'city']
        db.delete_unique('fccpublicfiles_address', ['address1', 'address2', 'state', 'zipcode', 'city'])


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
        'fccpublicfiles.address': {
            'Meta': {'unique_together': "(('address1', 'address2', 'city', 'state', 'zipcode'),)", 'object_name': 'Address'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_labels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fccpublicfiles.AddressLabel']", 'symmetrical': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'fccpublicfiles.addresslabel': {
            'Meta': {'object_name': 'AddressLabel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'fccpublicfiles.broadcaster': {
            'Meta': {'object_name': 'Broadcaster'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['fccpublicfiles.Address']", 'null': 'True', 'blank': 'True'}),
            'callsign': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'channel': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'community_city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'community_state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'facility_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facility_type': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network_affiliate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nielsen_dma': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        'fccpublicfiles.organization': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organization'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['fccpublicfiles.Address']", 'null': 'True', 'blank': 'True'}),
            'employees': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fccpublicfiles.Person']", 'through': "orm['fccpublicfiles.Role']", 'symmetrical': 'False'}),
            'fec_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organization_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        'fccpublicfiles.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'fccpublicfiles.politicalbuy': {
            'Meta': {'object_name': 'PoliticalBuy', '_ormbases': ['fccpublicfiles.PublicDocument']},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'advertiser_politicalbuys'", 'null': 'True', 'to': "orm['fccpublicfiles.Organization']"}),
            'advertiser_signatory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Person']", 'null': 'True', 'blank': 'True'}),
            'bought_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mediabuyer_politicalbuys'", 'null': 'True', 'to': "orm['fccpublicfiles.Organization']"}),
            'contract_end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 11, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'contract_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'contract_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 11, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'lowest_unit_price': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'publicdocument_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fccpublicfiles.PublicDocument']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fccpublicfiles.politicalspot': {
            'Meta': {'object_name': 'PoliticalSpot'},
            'airing_days': ('weekday_field.fields.WeekdayField', [], {'max_length': '14', 'blank': 'True'}),
            'airing_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'airing_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'broadcast_length': ('timedelta.fields.TimedeltaField', [], {'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.PoliticalBuy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_spots': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preemptable': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'show_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'timeslot_begin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'timeslot_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'fccpublicfiles.publicdocument': {
            'Meta': {'object_name': 'PublicDocument'},
            'documentcloud_doc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doccloud.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'station': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'fccpublicfiles.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fccpublicfiles']