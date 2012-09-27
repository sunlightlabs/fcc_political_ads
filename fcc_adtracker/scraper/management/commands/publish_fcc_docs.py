from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from scraper.models import PDF_File
from scraper.create_ad_buys import make_ad_buy_from_pdf_file




class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        files = PDF_File.objects.all()
        count = 0
        for afile in files:
            count += 1
            print "%s Running load %s " % (count, afile)
            result = make_ad_buy_from_pdf_file(afile)
            
            

            