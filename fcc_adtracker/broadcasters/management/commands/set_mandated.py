

from django.core.management.base import BaseCommand, CommandError

from broadcasters.models import Broadcaster
from scraper.models import StationData

class Command(BaseCommand):
    help = "One off to set mandated flag on broadcasters from station info"
    requires_model_validation = False
    
    def handle(self, *args, **options):
        all_mandated_broadcasters  = StationData.objects.filter(is_mandated_station=True)
        
        for broadcaster in all_mandated_broadcasters:
            #print "Setting mandated flag on %s" % broadcaster.facility_id
            try:
                this_broadcaster = Broadcaster.objects.get(facility_id=broadcaster.facility_id)
                this_broadcaster.is_mandated = True
                this_broadcaster.save()
            except Broadcaster.DoesNotExist:
                print "Missing station %s %s market: %s affiliation: %s" % (broadcaster.facility_id, broadcaster.callSign, broadcaster.nielsenDma, broadcaster.networkAfil)
        