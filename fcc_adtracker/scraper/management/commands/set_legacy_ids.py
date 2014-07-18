""" One-off to set ids, help start untying the two-id problem. """

import re

from scraper.models import PDF_File
from django.core.paginator import Paginator
from django.core.management.base import BaseCommand, CommandError


fcc_infile_identifier = re.compile(r'\((\d{14})\)_.pdf')
fcc_id_re = re.compile(r'\((\d{14})\)')

def set_underscored_ids():
    chunk_size = 1000
    
    row_num = 0
    
    all_rows = PDF_File.objects.filter(raw_url__contains=")_.pdf", alternate_id__isnull=True).order_by('pk')
    paginator = Paginator(all_rows, chunk_size)
    print "Processing %s underscored rows" % (paginator.count)
    file_rows = []
    
    for this_page in paginator.page_range:
        print "Processing %s" % (this_page)
        for row in paginator.page(this_page).object_list:
            if row_num%100==0:
                print "Processed %s rows" % (row_num)
        
            row_num += 1
        
        
        
            this_url = row.raw_url
            fccidfound = re.search(fcc_infile_identifier, this_url)
            if fccidfound:
                underscored_id = fccidfound.group(1)
                row.alternate_id = underscored_id
                row.save()
            else:
                print "No fcc underscore id found in %s" % (this_url)


def set_fcc_ids():
    chunk_size = 1000

    row_num = 0

    all_rows = PDF_File.objects.filter(raw_url__contains=").pdf", file_id__isnull=True).order_by('pk')
    paginator = Paginator(all_rows, chunk_size)
    print "Processing %s non_underscored rows" % (paginator.count)
    file_rows = []

    for this_page in paginator.page_range:
        print "Processing %s" % (this_page)
        for row in paginator.page(this_page).object_list:
            if row_num%100==0:
                print "Processed %s rows" % (row_num)

            row_num += 1



            this_url = row.raw_url
            fccidfound = re.search(fcc_id_re, this_url)
            if fccidfound:
                this_id = fccidfound.group(1)
                row.file_id = this_id
                row.save()
            else:
                print "No fcc id found in %s" % (this_url)


class Command(BaseCommand):
    help = "Set underscored ids when applicable; set regular ids when applicable"
    requires_model_validation = False
    
   
    
    def handle(self, *args, **options):
        set_underscored_ids()
        set_fcc_ids()        
