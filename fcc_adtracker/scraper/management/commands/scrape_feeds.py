# Scrape many feeds to recover id information that may have been lost. 

from optparse import make_option


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from scraper.feed_handler_utils import handle_feed_url
from scraper.fcc_scraper import folder_placeholder
from scraper.utils import mandated_stations
from scraper.models import PDF_File

FCC_SCRAPER_LOG_DIRECTORY = getattr(settings, 'FCC_SCRAPER_LOG')
YEARS_WE_CARE_ABOUT = [ '2014']

class Command(BaseCommand):        
        
        
        args = '<search_string ...>'
        help = 'Scrape the FCC site for PDF\'s of political ad buys. With no arguments, will scrape every station. If given the URL of a folder, will scrape that folder. Logs to %s' % (FCC_SCRAPER_LOG_DIRECTORY)
        can_import_settings = True

        option_list = BaseCommand.option_list + (
            make_option('-n', '--non-recursive',
                        action='store_false',
                        dest='process_recursively',
                        default=True,
                        help='Only process the folder(s) given, not their children'),
            )


        def handle(self, *args, **options):
            process_recursively = options.get('process_recursively')

            if (len(args) == 0):
                #all_station_values = PDF_File.objects.all().order_by('callsign').values('callsign').distinct()
                all_station_values = ['KYW-TV', 'WCAU', 'WFMZ', 'WMGM-TV', 'WPHL-TV', 'WPSG', 'WPVI-TV', 'WTVE', 'WTXF-TV', 'WUVP-DT', 'WWSI'] 
                for this_station in all_station_values:
                    #this_callsign = this_station['callsign']
                    this_callsign = this_station
                    for year in YEARS_WE_CARE_ABOUT:
                        print "\n\nProcessing %s : %s - logs to: %s" % (year, this_callsign, FCC_SCRAPER_LOG_DIRECTORY)
                        url = "https://stations.fcc.gov/station-profile/%s/political-files/browse->%s" % (this_callsign, year)
                        this_folder = folder_placeholder(url, 'root', this_callsign)
                        this_folder.process_feeds(process_recursively)

            elif len(args) > 0:
                url_array = []
                for this_callsign in args:
                    for year in YEARS_WE_CARE_ABOUT:
                        print "\n\nProcessing %s : %s - logs to: %s" % (year, this_callsign, FCC_SCRAPER_LOG_DIRECTORY)
                        url = "https://stations.fcc.gov/station-profile/%s/political-files/browse->%s" % (this_callsign, year)
                        this_folder = folder_placeholder(url, 'root', this_callsign)
                        this_folder.process_feeds(process_recursively)


            else:
                raise CommandError('Invalid arguments')
                
            
