import urllib2
import urllib
from time import sleep

try:
    import json
except ImportError:
    import simplejson as json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from scraper.models import doc_source, dc_reference
from broadcasters.models import Broadcaster

SEARCH_URL_EXPR = getattr(settings, 'SEARCH_URL_EXPR')

class Command(BaseCommand):
    
    requires_model_validation = False
    can_import_settings = True
    
    def handle(self, *args, **options):
        source = doc_source.objects.get(pk=1)
        
        total = None
        not_last_page = True
        page = 1
        # max is 1000
        results_per_page = 1000
        num_pages = 1
        
        base_url = SEARCH_URL_EXPR % results_per_page
        while not_last_page:
            url = base_url + str(page)
            print "Grabbing %s" % url
            data = urllib2.urlopen(url).read()
            data_read = json.loads(data)


            #print data_read
            for doc in data_read['documents']:
                docid = doc['id']
                title = doc['title']
                
                (dcref, created) = dc_reference.objects.get_or_create(dc_slug=docid, defaults={'dc_title':title, 'source':source})
                
                if created:
                    print "Created dc reference: %s" % title



            if not total:
                total = data_read['total']
                num_pages = total / results_per_page 
                # Do we have an orpan last page? 
                if (total % results_per_page > 0):
                    num_pages+= 1
                    
            if (page == num_pages ):
                not_last_page = False

            print "Got page %s of %s (page_size = %s) ; now sleeping 2 secs" % (page, num_pages, results_per_page)
            page += 1    
            sleep(2)