from django.core.management.base import BaseCommand, CommandError

from scraper.models import ftf_reference
from fccpublicfiles.models import PoliticalBuy


class Command(BaseCommand):
    help = "Set totals that propublica has collected, if they're available"
    
    requires_model_validation = False
    
    def handle(self, *args, **options):
        freedfiles = ftf_reference.objects.filter(status='Freed File')
        freefilecount = 0
        missingfiles = 0
        ads_updated = 0
        
        for freefile in freedfiles:
            #print "Got free file %s" % (freefile.doc_id)
            freefilecount+= 1
            
            
            try:
                thisbuy = PoliticalBuy.objects.get(is_FCC_doc=True, related_FCC_file__raw_url__contains=freefile.doc_id)
#pp_data_ref__isnull=True
                #print "Found file: %s" % (freefile.doc_id)
                amt = thisbuy.total_spent_raw
                contract = thisbuy.contract_number
                needs_saving = False
                if not amt:
                    thisbuy.total_spent_raw = freefile.v_amt
                    thisbuy.using_pp_data = True
                    needs_saving = True
                if not contract:
                    thisbuy.contract_number = freefile.v_contract_no
                    thisbuy.using_pp_data = True
                    needs_saving = True
                if not thisbuy.pp_data_ref:
                    thisbuy.pp_data_ref = freefile
                    needs_saving = True
                if needs_saving:
                    ads_updated += 1
                    thisbuy.save_no_update()
                
            except:
                #print "Failed on %s" % (freefile.doc_id)
                missingfiles +=1
                
        
        print "Total freed files: %s - missing files %s. Ads updated = %s" % (freefilecount, missingfiles, ads_updated)
        
        not_ad_buy_count = 0
        ads_updated = 0
        not_ad_buys = ftf_reference.objects.filter(status='Not an ad buy')
        for non_ad in not_ad_buys:
            not_ad_buy_count += 1
            thisbuy = None
            try:
                thisbuy = PoliticalBuy.objects.get(is_FCC_doc=True, related_FCC_file__raw_url__contains=non_ad.doc_id)
            except:
                continue                
            if not thisbuy.is_invoice or thisbuy.is_invalid:
                # don't call it invalid if we've already entered it..
                if not thisbuy.num_spots_raw:
                    thisbuy.is_invalid = True
                    thisbuy.pp_data_ref = non_ad
                    thisbuy.using_pp_data = True
                    thisbuy.save_no_update()
                    ads_updated += 1

                    
        print "Found %s non ad buys. %s ads updated." % (not_ad_buy_count, ads_updated)
                
            