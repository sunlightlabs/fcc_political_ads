""" Run this *after* populating committees from ad hawk. Collects all the committees that aren't linked to from an ad hawk advertiser and adds them """

from django.core.management.base import BaseCommand, CommandError
from fecdata.models import Committee, Candidate
from fccpublicfiles.models import TV_Advertiser

class Command(BaseCommand):
    args = '<cycle>'
    help = "Create tv_advertisers from committees that aren't defined in ad hawk with their FEC data"
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        assigned_committee_hash = {}
        
        # populate committee hash with committees already assigned
        all_advertisers = TV_Advertiser.objects.all()
        for advertiser in all_advertisers:
            if advertiser.primary_committee:
            # not all advertisers have committees associate with them
                assigned_committee_hash[advertiser.primary_committee.fec_id] = 1
            for secondary_committee in advertiser.secondary_committees.all():
                assigned_committee_hash[advertiser.primary_committee.fec_id] = 1
        
        # Add missing committees
        all_committees = Committee.objects.all()
        for committee in all_committees:
            try:
                assigned_committee_hash[committee.fec_id]
            except KeyError:
                #print "Need to add committee %s" % committee.name
                
                if committee.related_candidate:
                    print "%s has candidate %s" % (committee.name, committee.related_candidate.fec_name)
                    TV_Advertiser.objects.get_or_create(advertiser_name=committee.name, defaults={
                        'candidate':committee.related_candidate,
                        'candidate_name':committee.related_candidate.fec_name,
                        'committee_name':committee.name,
                        'primary_committee':committee,
                    })
        
                else:
                    TV_Advertiser.objects.get_or_create(advertiser_name=committee.name, defaults={
                        'committee_name':committee.name,
                        'advertiser_name':committee.name,
                        'primary_committee':committee,
                    })
        