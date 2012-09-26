from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from scraper.models import PDF_File
from scraper.create_ad_buys import make_ad_buy_from_pdf_file


num_to_load = 5

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        files = PDF_File.objects.exclude(in_document_cloud=True).order_by('-upload_time')[:num_to_load]
        count = 0
        for afile in files:
            count += 1
            print "%s Running load %s " % (count, afile)
            result = make_ad_buy_from_pdf_file(afile)
            
            

            