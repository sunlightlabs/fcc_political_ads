import urllib2
import pytz

from time import sleep
from urlparse import urlparse
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from scraper.models import PDF_File
from scraper.utils import read_url


utc=pytz.UTC

try:
    pass
    SCRAPER_LOCAL_DOC_DIR = getattr(settings, 'SCRAPER_LOCAL_DOC_DIR')
except:
    raise Exception("missing local setting: SCRAPER_LOCAL_DOC_DIR")


class Command(BaseCommand):
    
    requires_model_validation = False
    can_import_settings = True
    
    def handle(self, *args, **options):
        pdfs_to_backup = PDF_File.objects.filter(local_file_path__isnull=True).exclude(not_at_fcc=True).values('id')
        
        num_to_process = len(pdfs_to_backup)
        print "Processing %s files" % num_to_process
        count = 0 
        
        for this_pdf_id in pdfs_to_backup:
            this_pdf = PDF_File.objects.get(pk=this_pdf_id['id'])
            
            if this_pdf.local_file_path or this_pdf.not_at_fcc:
                print "already entered!"
                continue
            
            count += 1
            pdf_url = this_pdf.raw_url
            
            tempfile_name =  urllib2.unquote(urlparse(pdf_url).path)
            tempfile_name = tempfile_name.lstrip('/')
            tempfile_name_fixed = tempfile_name.replace("/", "%%")
            if count%3 == 0: 
                print "Processed %s" % count
            
            try:
                page = read_url(pdf_url)
            except urllib2.HTTPError:
                print "Couldn't get file %s" % (pdf_url)
                this_pdf.not_at_fcc=True
                this_pdf.missing_as_of_date=datetime.now()
                this_pdf.save()
                continue
            
            #print "read the pdf"
            
            tempfile_full = SCRAPER_LOCAL_DOC_DIR + "/" + tempfile_name_fixed
            tempfile = open(tempfile_full, "wb")
            tempfile.write(page)
            this_pdf.local_file_path = tempfile_name_fixed
            this_pdf.save()
            tempfile.close()
            #print "wrote the pdf to %s" % (tempfile_full)
            
            sleep(0.5)
            