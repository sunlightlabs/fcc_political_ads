""" Match up doc titles to extract correct dc slugs.   
This is not perfect... 
"""
import re

from django.core.management.base import BaseCommand, CommandError

from scraper.models import PDF_File, dc_reference
from broadcasters.models import Broadcaster
from fccpublicfiles.models import PoliticalBuy


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
                continue
            
            try:
                dc_file = dc_reference.objects.get(dc_title__icontains=our_title)
                print "** Found match for %s: %s" % (our_title, dc_file.dc_slug)
                total_matches += 1
                orphan.dc_slug = dc_file.dc_slug
                orphan.dc_title = dc_file.dc_title
                orphan.in_document_cloud = True
                orphan.save()
                
                
            except (dc_reference.DoesNotExist, dc_reference.MultipleObjectsReturned):
                orphan.in_document_cloud = False
                orphan.save()
                print "** No match for %s" % (our_title)
                
        missing_adbuys = PoliticalBuy.objects.filter(is_FCC_doc=True, in_document_cloud=False, related_FCC_file__in_document_cloud=True)
        for adbuy in missing_adbuys:
            adbuy.in_document_cloud = True
            adbuy.save_no_update()
            
            
                
        print "Found %s of %s docs" % (total_matches, total)