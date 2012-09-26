""" Match up doc titles to extract correct dc slugs.   
This is not perfect... 
"""

from django.core.management.base import BaseCommand, CommandError

from scraper.models import PDF_File, dc_reference
from broadcasters.models import Broadcaster

class Command(BaseCommand):
    
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        orphan_pdfs = PDF_File.objects.filter(dc_slug__isnull=True)
        total = 0
        total_matches = 0
        for orphan in orphan_pdfs:
            total += 1
            our_url = orphan.raw_url
            our_title = our_url.replace("https://stations.fcc.gov/collect/files/", "")
            #print "Processing '%s' " % our_title
            
            try:
                dc_file = dc_reference.objects.filter(dc_title__icontains=our_title)[0]
                #print "** Found match for %s: %s" % (our_title, dc_file.dc_slug)
                total_matches += 1
                orphan.dc_slug = dc_file.dc_slug
                orphan.dc_title = dc_file.dc_title
                orphan.in_document_cloud = True
                orphan.save()
            except IndexError:
                orphan.in_document_cloud = False
                orphan.save()
                print "** No match for %s" % (our_title)
                
        print "Found %s of %s docs" % (total_matches, total)