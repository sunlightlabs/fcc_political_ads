# Scrape only the base feed url -- all the child feed urls appear to be broken. 

 

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from scraper.feed_handler_utils import handle_feed_url
from scraper.models import PDF_File

FCC_SCRAPER_LOG_DIRECTORY = getattr(settings, 'FCC_SCRAPER_LOG')


# As of 8/15/14 all feeds are broken except for the station root feeds
def get_working_station_feed_url(callsign):
    feed_url = "https://stations.fcc.gov/station-profile/%s/rss/" % (callsign)
    return feed_url
    
class Command(BaseCommand):        
        
        
        def handle(self, *args, **options):
            #all_station_values = PDF_File.objects.all().order_by('callsign').values('callsign').distinct()
            all_station_values = PDF_File.objects.filter(callsign__gte='KMGH-TV').order_by('callsign').values('callsign').distinct()
            for this_station in all_station_values:
                this_callsign = this_station['callsign']
                feed_url = get_working_station_feed_url(this_callsign)
                print "handling feed %s" % feed_url
                handle_feed_url(feed_url)
                
        
