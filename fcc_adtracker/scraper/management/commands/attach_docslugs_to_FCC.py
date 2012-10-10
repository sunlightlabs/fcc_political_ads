""" Match up doc titles to extract correct dc slugs.   
This is not perfect... 
"""
import re

from django.core.management.base import BaseCommand, CommandError

from scraper.models import PDF_File, dc_reference
from broadcasters.models import Broadcaster


class Command(BaseCommand):
    
    requires_model_validation = False
    
    def handle(self, *args, **options):
        fcc_identifier = re.compile(r'\((\d{14}\))')
        
        orphan_pdfs = PDF_File.objects.filter(dc_slug__isnull=True)
        total = 0
        total_matches = 0
        for orphan in orphan_pdfs:
            total += 1
            our_title = orphan.file_name()
            print "Processing %s" % our_title
            # get FEC's 14-digit id
            fcc_id = re.search(fcc_identifier, our_title)
            if fcc_id:
                print "Found id  %s in '%s' " % (fcc_id.group(0), our_title)
            else:
                print "*** no match in %s" % (our_title)
                assert False
                continue
            
            try:
                dc_file = dc_reference.objects.get(dc_title__icontains=our_title)
                print "** Found match for %s: %s" % (our_title, dc_file.dc_slug)
                total_matches += 1
                orphan.dc_slug = dc_file.dc_slug
                orphan.dc_title = dc_file.dc_title
                orphan.in_document_cloud = True
                orphan.save()
            except dc_reference.DoesNotExist:
                orphan.in_document_cloud = False
                orphan.save()
                print "** No match for %s" % (our_title)
                
                
            
                
        print "Found %s of %s docs" % (total_matches, total)