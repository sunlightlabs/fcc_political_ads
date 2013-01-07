# Note: Gotta put quotes around single URL's if processing one at a time
# https://stations.fcc.gov/station-profile/ksgw-tv/political-files/browse->2012
# The > in the url breaks the command line

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from optparse import make_option

from scraper.fcc_scraper import folder_placeholder
from scraper.utils import mandated_stations, parse_folder_url

FCC_SCRAPER_LOG_DIRECTORY = getattr(settings, 'FCC_SCRAPER_LOG')

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
                        
            for this_callsign in mandated_stations:
                # There's confusion as to when files need to get uploaded
                for year in (2012, 2013):
                    print "\n\nProcessing %s : %s - logs to: %s" % (year, this_callsign, FCC_SCRAPER_LOG_DIRECTORY)
                    url = "https://stations.fcc.gov/station-profile/%s/political-files/browse->%s" % (this_callsign, year)
                    this_folder = folder_placeholder(url, 'root', this_callsign)
                    this_folder.process(process_recursively)
                
        elif len(args) > 0:
            url_array = []
            for arg in args:
                url_to_process = args[0]
                url_to_process = url_to_process.replace("%3E", ">")
                (callSign, pathArray) = parse_folder_url(url_to_process)
                if not callSign:
                    raise CommandError("Couldn't find callsign in folder URL: %s" % (url_to_process))
                url_array.append({'url':url_to_process, 'callSign':callSign})
                
            for this_url in url_array:
                print "\n\nProcessing %s - logs to: %s" % (this_url, FCC_SCRAPER_LOG_DIRECTORY)
                this_folder = folder_placeholder(this_url['url'], 'manual process', this_url['callSign'])
                this_folder.process(process_recursively)
        
            
        else:
            raise CommandError('Invalid arguments')