# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ftf_reference'
        db.create_table('scraper_ftf_reference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('callsign', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('market', self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True)),
            ('v_committee', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('v_amt', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('v_agncy', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('v_contract_no', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('pp_scrape_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('fcc_upload_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('fcc_metadata', self.gf('django.db.models.fields.CharField')(max_length=511, null=True, blank=True)),
            ('file_url', self.gf('django.db.models.fields.CharField')(max_length=511, null=True, blank=True)),
            ('doc_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('scraper', ['ftf_reference'])


    def backwards(self, orm):
        # Deleting model 'ftf_reference'
        db.delete_table('scraper_ftf_reference')


    models = {
        'broadcasters.broadcaster': {
            'Meta': {'ordering': "('community_state', 'community_city', 'callsign')", 'object_name': 'Broadcaster'},
            'callsign': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'channel': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'community_city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'community_state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'dma_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facility_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facility_type': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mandated': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'network_affiliate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nielsen_dma': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        'scraper.dc_reference': {
            'Meta': {'object_name': 'dc_reference'},
            'dc_slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dc_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraper.doc_source']", 'null': 'True'})
        },
        'scraper.dma_summary': {
            'Meta': {'object_name': 'dma_summary'},
            'dma_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dma_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fcc_dma_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'house_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_broadcasters': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outside_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pres_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rank1011': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rank1112': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recent_house_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recent_outside_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recent_pres_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recent_sen_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sen_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tot_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'scraper.doc_source': {
            'Meta': {'object_name': 'doc_source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'raw_html': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'use_html': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '255'})
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
        'scraper.ftf_reference': {
            'Meta': {'object_name': 'ftf_reference'},
            'callsign': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'doc_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fcc_metadata': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'fcc_upload_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'file_url': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'market': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'pp_scrape_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'v_agncy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'v_amt': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'v_committee': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'v_contract_no': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'})
        },
        'scraper.pdf_file': {
            'Meta': {'object_name': 'PDF_File'},
            'ad_type': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'callsign': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'community_state': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'dc_slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dc_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dma_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facility_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'federal_district': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'federal_office': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraper.Folder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_document_cloud': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'nielsen_dma': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'raw_name_guess': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'raw_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '511'}),
            'related_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'related_pac_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'upload_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'scraper.scrape_time': {
            'Meta': {'object_name': 'Scrape_Time'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'scraper.state_summary': {
            'Meta': {'object_name': 'state_summary'},
            'house_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_broadcasters': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outside_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pres_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recent_house_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recent_outside_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recent_pres_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recent_sen_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sen_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'tot_buys': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
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