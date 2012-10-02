""" One off to deal with organizations. """

from django.core.management.base import BaseCommand, CommandError
from fccpublicfiles.models import TV_Advertiser, Organization


# only set names once we've finished manual cleanup. 
save_changes=True

class Command(BaseCommand):
    args = '<cycle>'
    help = "point orgs at advertisers; also diagnose stuff to be merged with save_changes set to false."
    requires_model_validation = False
    
    
    def handle(self, *args, **options):
        
        # diagnose problems for manual fixes
        for adv in Organization.objects.filter(organization_type__exact='AD'):
            print "adv is: %s" % adv.name
            
            try:
                this_tv_adv = TV_Advertiser.objects.get(primary_committee__fec_id=adv.fec_id)
                #print "Found TV Advertiser %s" % ()
                newname = this_tv_adv.advertiser_name
                if (this_tv_adv.candidate):
                    newname = newname + " (SUPPORTS %s)" % this_tv_adv.candidate_name
                print "New name is %s" % newname
                
                if (save_changes):
                    adv.name = newname
                    adv.related_advertiser = this_tv_adv
                    adv.save(None)

                    
                
            except TV_Advertiser.DoesNotExist:
                print "Missing TV Advertiser %s with id: '%s'" % (adv.name, adv.fec_id)
                
                try:
                    TV_Advertiser.objects.get(secondary_committee__fec_id=adv.fec_id)
                    print "SECONDARY ADV FOUND!"
                    
                except:
                    print "** missing secondary adv too."
                    
        # If the only stuff missing is entries with n            
            