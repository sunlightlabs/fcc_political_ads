# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django_extensions.db.fields import UUIDField
from uuid import uuid4


class Migration(SchemaMigration):

    def forwards(self, orm):

        db.execute_many("""
        set constraints all deferred;

        -- set up the schema to accept new ids, putting the UUIDs in new placeholder columns
        alter table fccpublicfiles_politicalbuy add column new_id uuid default(uuid_generate_v4()) unique;
        alter table fccpublicfiles_politicalspot add column politicalbuy_id uuid references fccpublicfiles_politicalbuy (new_id) deferrable initially deferred;
        alter table fccpublicfiles_politicalbuy_broadcasters rename politicalbuy_id to politicalbuy_id_old;
        alter table fccpublicfiles_politicalbuy_broadcasters add column politicalbuy_id uuid references fccpublicfiles_politicalbuy (new_id) deferrable initially deferred;

        -- migrate the data
        update fccpublicfiles_politicalspot as ps set politicalbuy_id = pb.new_id from fccpublicfiles_politicalbuy pb where pb.id = ps.document_id;
        update fccpublicfiles_politicalbuy_broadcasters as pbbc set politicalbuy_id = new_id from fccpublicfiles_politicalbuy pb where pb.id = pbbc.politicalbuy_id_old;
        
        set constraints all immediate;

        -- drop old fk's depending on old pk
        alter table fccpublicfiles_politicalbuy_broadcasters drop column politicalbuy_id_old;
        alter table fccpublicfiles_politicalspot drop column document_id;

        -- drop pk constraint and then the column
        alter table fccpublicfiles_politicalbuy drop constraint fccpublicfiles_politicalbuy_pkey;
        alter table fccpublicfiles_politicalbuy drop column id;
        
        -- move new id into permanent place
        alter table fccpublicfiles_politicalbuy rename new_id to id;
        alter table fccpublicfiles_politicalbuy add primary key (id);
        """)

    def backwards(self, orm):
        pass


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
            'employees': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fccpublicfiles.Person']", 'through': "orm['fccpublicfiles.Role']", 'symmetrical': 'False'}),
            'fec_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organization_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        'fccpublicfiles.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'fccpublicfiles.politicalbuy': {
            'Meta': {'object_name': 'PoliticalBuy'},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'advertiser_politicalbuys'", 'null': 'True', 'to': "orm['fccpublicfiles.Organization']"}),
            'advertiser_signatory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Person']", 'null': 'True', 'blank': 'True'}),
            'bought_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mediabuyer_politicalbuys'", 'null': 'True', 'to': "orm['fccpublicfiles.Organization']"}),
            'broadcasters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['broadcasters.Broadcaster']", 'null': 'True', 'symmetrical': 'False'}),
            'contract_end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True', 'blank': 'True'}),
            'contract_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'contract_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'documentcloud_doc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doccloud.Document']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lowest_unit_price': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'total_spent_raw': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'fccpublicfiles.politicalspot': {
            'Meta': {'object_name': 'PoliticalSpot'},
            'airing_days': ('weekday_field.fields.WeekdayField', [], {'max_length': '14', 'blank': 'True'}),
            'airing_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'airing_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'broadcast_length': ('timedelta.fields.TimedeltaField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.PoliticalBuy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_spots': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preemptable': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'show_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'timeslot_begin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'timeslot_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'fccpublicfiles.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fccpublicfiles.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
