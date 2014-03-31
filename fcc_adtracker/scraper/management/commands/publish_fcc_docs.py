# to do -- make this routine more efficient--don't save stuff with no changes. 

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django.db import connection

from scraper.models import PDF_File
from scraper.create_ad_buys import make_ad_buy_from_pdf_file
c = connection.cursor()



class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        files = PDF_File.objects.all()

        efficient_query_for_ids = """select scraper_pdf_file.id from scraper_pdf_file left join fccpublicfiles_politicalbuy on scraper_pdf_file.id = fccpublicfiles_politicalbuy."related_FCC_file_id" where fccpublicfiles_politicalbuy."related_FCC_file_id" is null;"""
        c.execute(efficient_query_for_ids)
        results = c.fetchall()
        
        for count, result in enumerate(results):
            print "%s Running load %s " % (count, result[0])
            result = make_ad_buy_from_pdf_file(result[0])
            
            

            