import sys
import csv

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.conf import settings

from fccpublicfiles.models import PoliticalBuy
from scraper.models import Scrape_Time

AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY =  getattr(settings, 'AWS_SECRET_ACCESS_KEY')
CSV_EXPORT_DIR =  getattr(settings, 'CSV_EXPORT_DIR')

def write_csv_to_file(file_description, local_file, fields, rows):
    local_response = open(local_file, 'w')
    writer = csv.writer(local_response)
    writer.writerow([file_description])
    writer.writerow(fields)
    for row in rows:
        writer.writerow(row)
    

def all_ads_to_file():
    most_recent_scrape=Scrape_Time.objects.all().order_by('-run_time')[0].run_time
    file_description="This file contains ads uploaded by volunteers and from the FCC's site available as of %s" % most_recent_scrape.strftime("%Y-%m-%d %H:%m")
    print file_description
    file_name =  "%s/all_ad_buys.csv" % (CSV_EXPORT_DIR)
    fields = ['id', 'station', 'file_upload_date', 'tv_market', 'tv_market_id', 'ad_type', 'fcc_folder', 'file_name', 'source_file_url', 'advertiser_name', 'is_invalid', 'is_invoice', 'total_spent_raw', 'num_spots_raw', 'contract_number', 'source']
    all_rows = PoliticalBuy.objects.all()
    file_rows = []
    for row in all_rows:
        
        raw_url = ""
        this_file_name = ""
        
        if row.is_FCC_doc:
            related_doc = row.related_FCC_file
            raw_url = related_doc.raw_url
            this_file_name = related_doc.file_name()
        else:
            raw_url = row.documentcloud_doc.get_absolute_url()
        is_invalid = ""
        is_invoice = ""
        
        if (row.is_invalid):
            is_invalid = 'Y'

        if (row.is_invoice):
            is_invoice = 'Y'        
        
        file_rows.append([row.pk, row.broadcaster_callsign, row.upload_time.strftime("%Y-%m-%d"), row.nielsen_dma, row.dma_id, row.candidate_type, row.fcc_folder_name, this_file_name, raw_url, row.advertiser_display_name, is_invalid, is_invoice, row.total_spent_raw, row.num_spots_raw, row.contract_number, row.doc_source()])
    
    write_csv_to_file(file_description, file_name, fields, file_rows)
    

class Command(BaseCommand):
    help = "Dump the big files to a predefined spot in the filesystem. They need to then get moved to S3"
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        b = conn.get_bucket('politicaladsleuth-assets')
        k = Key(b)
        
        print "Writing ads to file..."
        all_ads_to_file()
        
        for file_to_upload in (['all_ad_buys.csv']):
            print "pushing to S3: %s" % file_to_upload
            local_file_path = "%s/%s" % (CSV_EXPORT_DIR, file_to_upload)
            print local_file_path
            s3_string = "media/csv/%s" % file_to_upload
            k.key = s3_string
            k.set_contents_from_filename(local_file_path, policy='public-read')