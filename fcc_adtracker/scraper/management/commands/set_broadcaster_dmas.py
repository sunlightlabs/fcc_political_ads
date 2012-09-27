""" Set broadcaster DMA, DMA_ids from station data directly.  """
from django.core.management.base import BaseCommand, CommandError

from scraper.models import StationData
from broadcasters.models import Broadcaster


class Command(BaseCommand):
    
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        allbroadcasters = Broadcaster.objects.filter(dma_id__isnull=True)
        for broadcaster in allbroadcasters:
            try:
                sd = StationData.objects.get(facility_id=broadcaster.facility_id)
                broadcaster.nielsen_dma = sd.nielsenDma
                broadcaster.dma_id = sd.nielsenDma_id
                broadcaster.save()
            except sd.DoesNotExist:
                try:
                    sd = StationData.objects.get(callSign=broadcaster.callsign)
                    broadcaster.nielsen_dma = sd.nielsenDma
                    broadcaster.dma_id = sd.nielsenDma_id
                    broadcaster.save()
                except sd.DoesNotExist:
                    
                    
                    print "Couldn't find station data for broadcaster %s" % broadcaster
                    # The misses seem to be guam, pr, virgin islands, etc. 
            
