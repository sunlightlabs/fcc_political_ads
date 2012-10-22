import sys
import traceback

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from scraper.models import PDF_File
from scraper.local_log import fcc_logger

try:
    SCRAPER_LOCAL_DOC_DIR = getattr(settings, 'SCRAPER_LOCAL_DOC_DIR')
    AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY =  getattr(settings, 'AWS_SECRET_ACCESS_KEY')
except:
    raise Exception("missing local setting: SCRAPER_LOCAL_DOC_DIR or AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY")


class Command(BaseCommand):
    
    requires_model_validation = False
    can_import_settings = True
    
    def handle(self, *args, **options):
        
        
        my_logger=fcc_logger()
        my_logger.info("starting backup run...")
        
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        b = conn.get_bucket('politicaladsleuth-assets')
        k = Key(b)
        
        pdfs_to_backup = PDF_File.objects.filter(local_file_path__isnull=False, is_backed_up=False).values('id')

        num_to_process = len(pdfs_to_backup)
        
        print "Processing %s files" % num_to_process
        count = 0 

        for this_pdf_id in pdfs_to_backup:
            this_pdf = PDF_File.objects.get(pk=this_pdf_id['id'])

            if this_pdf.is_backed_up:
                print "already backed up!"
                continue
            
            count+=1
            if (count %100 == 0):
                print "Processed %s" % count
            local_file_path = this_pdf.local_file_path
            full_file_path = SCRAPER_LOCAL_DOC_DIR + "/" + local_file_path
            #print "path is: %s" % full_file_path
            
            local_file_path = local_file_path.replace("%%", "/")
            s3_string = "media/fcc_backup/%s" % local_file_path
            #print "s3 destination is: %s" % s3_string
            
            k.key = s3_string
            try:
                result = k.set_contents_from_filename(full_file_path, policy='public-read')
            except:
                tb = traceback.format_exc()
                message = "*BACKUP ERROR:* Error uploading %s\n%s" % (local_file_path, tb)
                print message
                my_logger.warn(message)

                continue
            this_pdf.is_backed_up = True
            this_pdf.s3_full_url = s3_string
            this_pdf.save()
            #print "result is %s" % result
            
        
        