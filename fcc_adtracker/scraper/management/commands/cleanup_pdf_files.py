from django.core.management.base import BaseCommand, CommandError

from scraper.models import Folder, PDF_File
from broadcasters.models import Broadcaster


class Command(BaseCommand):
    
    requires_model_validation = False
    
    def handle(self, *args, **options):
        allfiles = PDF_File.objects.all().select_related('folder', 'folder_broadcaster')
        for afile in allfiles:
            district = ""
            name = ""
            office = ""

            path = afile.path()
            if (path[1] == 'Non-Candidate Issue Ads'):
                is_outside_group = True 
            elif (path[1] == 'Federal'):
                office = path[2]
                if (office == 'US House'):
                    district = path[3]
            # They're not very consisten about this... 
            name = path[-2:-1][0]
            
            # hard truncate. This data's a mess.
            afile.ad_type =path[1]
            afile.federal_office = office[:31]
            afile.federal_district = district[:31]
            afile.raw_name_guess = name[:255]
            
            # flatten stuff
            afile.nielsen_dma = afile.folder.broadcaster.nielsen_dma
            afile.dma_id = afile.folder.broadcaster.dma_id
            afile.community_state = afile.folder.broadcaster.community_state
            
            afile.save()