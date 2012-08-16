# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Broadcaster'
        db.create_table('broadcasters_broadcaster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('callsign', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('channel', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('nielsen_dma', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('network_affiliate', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('facility_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True)),
            ('facility_type', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('community_city', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('community_state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('broadcasters', ['Broadcaster'])

        # Adding model 'BroadcasterAddress'
        db.create_table('broadcasters_broadcasteraddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('broadcaster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['broadcasters.Broadcaster'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Address'])),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.AddressLabel'])),
        ))
        db.send_create_signal('broadcasters', ['BroadcasterAddress'])

        # Adding unique constraint on 'BroadcasterAddress', fields ['broadcaster', 'address', 'label']
        db.create_unique('broadcasters_broadcasteraddress', ['broadcaster_id', 'address_id', 'label_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'BroadcasterAddress', fields ['broadcaster', 'address', 'label']
        db.delete_unique('broadcasters_broadcasteraddress', ['broadcaster_id', 'address_id', 'label_id'])

        # Deleting model 'Broadcaster'
        db.delete_table('broadcasters_broadcaster')

        # Deleting model 'BroadcasterAddress'
        db.delete_table('broadcasters_broadcasteraddress')


    models = {
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
        'broadcasters.broadcasteraddress': {
            'Meta': {'unique_together': "(('broadcaster', 'address', 'label'),)", 'object_name': 'BroadcasterAddress'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Address']"}),
            'broadcaster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['broadcasters.Broadcaster']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.AddressLabel']"})
        },
        'locations.address': {
            'Meta': {'unique_together': "(('address1', 'address2', 'city', 'state', 'zipcode'),)", 'object_name': 'Address'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'locations.addresslabel': {
            'Meta': {'object_name': 'AddressLabel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['broadcasters']