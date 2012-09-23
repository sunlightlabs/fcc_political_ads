from django.core.management.base import BaseCommand, CommandError

from scraper.models import Folder
from broadcasters.models import Broadcaster

class Command(BaseCommand):
    
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        all_folders = Folder.objects.all()
        for folder in all_folders:
            
            
            # Add a broadcaster if it's not there
            if not folder.broadcaster:
                #print "Missing broadcaster"
                thiscallsign = folder.callsign
                try:
                    thisbroadcaster = Broadcaster.objects.get(callsign__iexact=thiscallsign)
                    folder.broadcaster = thisbroadcaster
                    folder.save()
                except Broadcaster.DoesNotExist:
                    print "Couldn't find callsign %s" % (thiscallsign)
                    
            