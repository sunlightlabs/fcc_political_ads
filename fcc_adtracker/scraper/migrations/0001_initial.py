# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StationData'
        db.create_table('scraper_stationdata', (
            ('facility_id', self.gf('django.db.models.fields.CharField')(max_length=15, primary_key=True)),
            ('callSign', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('facilityType', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=31, null=True)),
            ('authAppId', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('band', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('virtualChannel', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('rfChannel', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('networkAfil', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('communityCity', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('communityState', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('nielsenDma', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('statusDate', self.gf('django.db.models.fields.DateField')(null=True)),
            ('licenseExpirationDate', self.gf('django.db.models.fields.DateField')(null=True)),
            ('partyName', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('partyAddress1', self.gf('django.db.models.fields.CharField')(max_length=127, null=True)),
            ('partyAddress2', self.gf('django.db.models.fields.CharField')(max_length=127, null=True)),
            ('partyCity', self.gf('django.db.models.fields.CharField')(max_length=127, null=True)),
            ('partyState', self.gf('django.db.models.fields.CharField')(max_length=7, null=True)),
            ('partyZip1', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('partyZip2', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('partyPhone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('studio_address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('studio_state', self.gf('django.db.models.fields.CharField')(max_length=7, null=True)),
            ('studio_zip', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('studio_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('station_lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('station_lng', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('nielsenDma_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('is_mandated_station', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('scraper', ['StationData'])

        # Adding model 'Folder'
        db.create_table('scraper_folder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('callsign', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('facility_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True)),
            ('broadcaster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['broadcasters.Broadcaster'], null=True, blank=True)),
            ('raw_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=511)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('scrape_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('folder_class', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
            ('folder_name', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
            ('related_candidate_id', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('related_pac_id', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('scraper', ['Folder'])

        # Adding model 'PDF_File'
        db.create_table('scraper_pdf_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('callsign', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('facility_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True)),
            ('folder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraper.Folder'])),
            ('raw_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=511)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('upload_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('related_candidate_id', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('related_pac_id', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('ad_type', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('federal_office', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('federal_district', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('raw_name_guess', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('in_document_cloud', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('scraper', ['PDF_File'])


    def backwards(self, orm):
        # Deleting model 'StationData'
        db.delete_table('scraper_stationdata')

        # Deleting model 'Folder'
        db.delete_table('scraper_folder')

        # Deleting model 'PDF_File'
        db.delete_table('scraper_pdf_file')


    models = {
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
        'scraper.folder': {
            'Meta': {'object_name': 'Folder'},
            'broadcaster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['broadcasters.Broadcaster']", 'null': 'True', 'blank': 'True'}),
            'callsign': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'facility_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'folder_class': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'folder_name': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '511'}),
            'related_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'related_pac_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'scrape_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'scraper.pdf_file': {
            'Meta': {'object_name': 'PDF_File'},
            'ad_type': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'callsign': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'facility_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'federal_district': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'federal_office': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraper.Folder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_document_cloud': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'raw_name_guess': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'raw_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '511'}),
            'related_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'related_pac_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'upload_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'scraper.stationdata': {
            'Meta': {'object_name': 'StationData'},
            'authAppId': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'band': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'callSign': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'communityCity': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'communityState': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'facilityType': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'facility_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'is_mandated_station': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'licenseExpirationDate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'networkAfil': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'nielsenDma': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'nielsenDma_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'partyAddress1': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True'}),
            'partyAddress2': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True'}),
            'partyCity': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True'}),
            'partyName': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'partyPhone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'partyState': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True'}),
            'partyZip1': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'partyZip2': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'rfChannel': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True'}),
            'station_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'station_lng': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'statusDate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'studio_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'studio_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'studio_state': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True'}),
            'studio_zip': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'virtualChannel': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['scraper']