# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Candidate'
        db.create_table('fecdata_candidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cycle', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('fec_id', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('fec_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('seat_status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('candidate_status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('state_address', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('state_race', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('campaign_com_fec_id', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
        ))
        db.send_create_signal('fecdata', ['Candidate'])

        # Adding model 'Committee'
        db.create_table('fecdata_committee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fec_id', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('treasurer', self.gf('django.db.models.fields.CharField')(max_length=38, null=True, blank=True)),
            ('street_1', self.gf('django.db.models.fields.CharField')(max_length=34, null=True, blank=True)),
            ('street_2', self.gf('django.db.models.fields.CharField')(max_length=34, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('state_race', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('designation', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('ctype', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('tax_status', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('filing_frequency', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('interest_group_cat', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('connected_org_name', self.gf('django.db.models.fields.CharField')(max_length=65, blank=True)),
            ('candidate_id', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('candidate_office', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('is_superpac', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('is_hybrid', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('is_nonprofit', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('related_candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fecdata.Candidate'], null=True)),
        ))
        db.send_create_signal('fecdata', ['Committee'])


    def backwards(self, orm):
        # Deleting model 'Candidate'
        db.delete_table('fecdata_candidate')

        # Deleting model 'Committee'
        db.delete_table('fecdata_committee')


    models = {
        'fecdata.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'campaign_com_fec_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'candidate_status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'cycle': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'fec_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'fec_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'seat_status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'state_address': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'state_race': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'fecdata.committee': {
            'Meta': {'object_name': 'Committee'},
            'candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'candidate_office': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'connected_org_name': ('django.db.models.fields.CharField', [], {'max_length': '65', 'blank': 'True'}),
            'ctype': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'fec_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'filing_frequency': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_group_cat': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'is_hybrid': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'is_nonprofit': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'is_superpac': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'related_candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fecdata.Candidate']", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'state_race': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'street_1': ('django.db.models.fields.CharField', [], {'max_length': '34', 'null': 'True', 'blank': 'True'}),
            'street_2': ('django.db.models.fields.CharField', [], {'max_length': '34', 'null': 'True', 'blank': 'True'}),
            'tax_status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'treasurer': ('django.db.models.fields.CharField', [], {'max_length': '38', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['fecdata']