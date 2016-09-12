""" This takes the place of the folder scraping routines that were built before there was an rss file available. """

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from scraper.rss_scraper import parse_xml_from_text, get_rss_from_web, get_rss_from_file
from scraper.models import PDF_File, StationData
from broadcasters.models import Broadcaster

FCC_SCRAPER_LOG_DIRECTORY = getattr(settings, 'FCC_SCRAPER_LOG')
from scraper.local_log import fcc_logger

my_logger=fcc_logger()
my_logger.info("starting fcc rss scrape...")

def handle_file(thisfile):
    print thisfile
    [callsign, nielsen_dma, dma_id, community_state] = [None, None, None, None]
    try:
        thisbroadcaster = Broadcaster.objects.get(facility_id=thisfile['facility_id'])
        callsign = thisbroadcaster.callsign
        nielsen_dma = thisbroadcaster.nielsen_dma
        community_state = thisbroadcaster.community_state
        dma_id = thisbroadcaster.dma_id
    except Broadcaster.DoesNotExist:
        pass

    if not callsign:
        callsign = thisfile['callsign']

    if thisfile['href']:
        (pdffile, created) = PDF_File.objects.get_or_create(raw_url=thisfile['href'],   defaults={'upload_time':thisfile['time_loaded'],'ad_type':thisfile['ad_type'][:31], 'federal_office':thisfile['federal_office'], 'federal_district':thisfile['federal_district'], 'facility_id':thisfile['facility_id'], 'callsign':callsign, 'nielsen_dma':nielsen_dma, 'dma_id':dma_id, 'community_state':community_state, 'raw_name_guess':thisfile['raw_name_guess'], 'file_id':thisfile['id'], 'alternate_id':thisfile['underscored_id'], 'quickview_folder_path':thisfile['full_folder_path'], 'document_title':thisfile['title']})
    else:
        message = "couldn't parse pdf file %s" % thisfile
        my_logger.warn(message)
        
class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        rssdata = get_rss_from_web()
        political_files = parse_xml_from_text(rssdata)
	print political_files
        for thisfile in political_files:
            handle_file(thisfile)
            
            
