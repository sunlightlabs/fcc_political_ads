# Scrape many feeds to recover id information that may have been lost. 

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from scraper.rss_scraper import get_rss, parse_xml_from_text, get_rss_from_file
from scraper.management.commands.scrape_fcc_rss import handle_file
from scraper.models import PDF_File, StationData
from broadcasters.models import Broadcaster



def handle_feed_url(feed_url, create_new=False):
    read = get_rss(feed_url)
    #read = get_rss_from_file()
    results = parse_xml_from_text(read)
    for result in results:
        print "handling %s id=%s alt_id=%s" % (result['title'], result['id'], result['underscored_id'])
        # we are seeing the underscored id. Look for the non-underscored id. 
        thisfile = None
        if result['id']:

            try:
                thisfile = PDF_File.objects.get(file_id=result['id'])
                print "Found file using id"
                
            except PDF_File.DoesNotExist:
                print "couldn't locate id: %s" % (result['id'])
                pass
                
        else:
            print "Missing id for %s" % (result['href'])
            continue
        
        if not thisfile and result['underscored_id']:
            try: 
                thisfile = PDF_File.objects.get(alternate_id=result['underscored_id'])
                print "Found file using alternate id"
            except PDF_File.DoesNotExist:
                print "Couldn't locate using alternate id"
                pass

        if thisfile:
            # we've retrieved the file, so now add data to it. 
            print "**Adding data"
            
            thisfile.document_title = result['title']
            thisfile.alternate_id = result['underscored_id']
            thisfile.file_id = result['id']
            thisfile.quickview_folder_path = result['full_folder_path']
            thisfile.underscore_url = result['href']
            
            thisfile.save()
        else:
            print "This file apparently doesn't exist %s" % (result['href'])
            if create_new:
                print "Creating new file for %s" % (result['href'])
                handle_file(result)

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):

        feed_url = "https://stations.fcc.gov/station-profile/kaal/rss/feed-/political_file/2014"
        feed_url = "https://stations.fcc.gov/station-profile/wkrc-tv/rss/feed-/political_file/2012/federal/us_senate/sherrod_brown/order_41246"
        handle_feed_url(feed_url)
