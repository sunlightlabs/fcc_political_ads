""" This takes the place of the folder scraping routines that were built before there was an rss file available. """

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from scraper.api_scraper import parse_api_feed
from scraper.models import PDF_File, StationData
from broadcasters.models import Broadcaster

FCC_SCRAPER_LOG_DIRECTORY = getattr(settings, 'FCC_SCRAPER_LOG')
from scraper.local_log import fcc_logger

my_logger=fcc_logger()
my_logger.info("starting fcc rss scrape...")

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        political_files = parse_api_feed()
        for thisfile in political_files:
            if not thisfile:
                # if there's no details, continue
                continue

            [callsign, nielsen_dma, dma_id, community_state] = [None, None, None, None]
            try:
                print("Facility id is: %s" % thisfile['facility_id'])
                thisbroadcaster = Broadcaster.objects.get(facility_id=thisfile['facility_id'])
                nielsen_dma = thisbroadcaster.nielsen_dma
                community_state = thisbroadcaster.community_state
                dma_id = thisbroadcaster.dma_id
            except Broadcaster.DoesNotExist:
                pass
            
            if thisfile['file_manager_id']:
                print("\n\n*****(((trying to create %s\n)))" % thisfile)
                
                (pdffile, created) = PDF_File.objects.get_or_create(\
                    raw_url=thisfile['raw_url'],   defaults={
                    'upload_time':thisfile['upload_time'],
                    'ad_type':thisfile['ad_type'], 
                    'federal_office':thisfile['federal_office'], 
                    'federal_district':thisfile['federal_district'], 
                    'facility_id':thisfile['facility_id'], 
                    'callsign':thisfile['callsign'], 
                    'nielsen_dma':nielsen_dma, 
                    'dma_id':dma_id, 'community_state':community_state, 
                    'raw_name_guess':thisfile['raw_name_guess'], 
                    'fcc_file_id':thisfile['fcc_file_id'],
                    'folder_id':thisfile['folder_id'],
                    'download_url':thisfile['download_url'],
                    'file_status':thisfile['file_status'],
                    'history_status':thisfile['history_status'],
                    'file_manager_id':thisfile['file_manager_id']
                    })
                if created:
                    print "\n\t\t Successfully created %s\n" % thisfile['download_url']
                else:
                    print "\n\t\t Did not create %s\ %sn" % (thisfile['download_url'], \
                        thisfile['file_manager_id'])
                
            else:
                message = "\n\n\t\t\tCouldn't parse pdf file %s" % thisfile
                my_logger.warn(message)
            