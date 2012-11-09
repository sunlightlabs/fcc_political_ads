import requests
import pytz
from time import sleep
from scraper.models import PDF_File

from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta


utc=pytz.UTC

class Command(BaseCommand):

    requires_model_validation = False
    can_import_settings = True

    def handle(self, *args, **options):
        a_day_ago = datetime.now() - timedelta(days=1)


        # REMINDER:
        # be nice to their servers when looping
        pdfs_to_backup = PDF_File.objects.exclude(not_at_fcc=True).values('id')
        count = 0 
        print "Processing %s files" % (len(pdfs_to_backup))
        for this_pdf_id in pdfs_to_backup:
            count += 1
            if count%100 == 0: 
                print "Processed %s" % count
            
            this_pdf = PDF_File.objects.get(pk=this_pdf_id['id'])
            
            raw_url = this_pdf.raw_url
            #print "URL: %s" % (raw_url)
            r = requests.head(url=raw_url)
            result = r.status_code
            #print result
            if result != 200:
                #print "not there"
                if not this_pdf.not_at_fcc:
                    print "Newly missing: %s" % (raw_url)
                    
                    this_pdf.not_at_fcc=True
                    this_pdf.missing_as_of_date=datetime.now()
                    this_pdf.save()
            else:
                if this_pdf.not_at_fcc:
                    print "Showed up again?! %s" % (raw_url)
            sleep(0.2)