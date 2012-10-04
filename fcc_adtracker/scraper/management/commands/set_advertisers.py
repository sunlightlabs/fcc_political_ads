from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from scraper.models import PDF_File
from scraper.create_ad_buys import make_ad_buy_from_pdf_file




class Command(BaseCommand):
    help = "Assign advertisers to PDF Files"
    
    def handle(self, *args, **options):
        
        files = PDF_File.objects.all()
        
        for this_file in files:
            
            foldername = this_file.raw_name_guess
            full_path = str(this_file)
            print "Processing <<%s>> '%s'" % (full_path, foldername)
        