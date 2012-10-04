# Need to attach advertiser type to ad buy.

from django.core.management.base import BaseCommand, CommandError

from fccpublicfiles.models import PoliticalBuy


class Command(BaseCommand):
    help = "We're treating ad buys as pdf files, so add identifying info about them from their broadcasters. Run regularly."
    requires_model_validation = False


    def handle(self, *args, **options):
        unattached_ad_buys = PoliticalBuy.objects.filter(dma_id__isnull=True, is_FCC_doc=False)
        
        for ad_buy in unattached_ad_buys:
            print ad_buy
            all_broadcasters = ad_buy.broadcasters.all()
            if len(all_broadcasters) > 0:
                first_broadcaster = all_broadcasters[0]
                
                ad_buy.nielsen_dma = first_broadcaster.nielsen_dma
                ad_buy.dma_id = first_broadcaster.dma_id
                ad_buy.community_state = first_broadcaster.community_state
                print "***setting dma:%s state %s" % (ad_buy.dma_id, ad_buy.community_state)
                
                # Don't let the system overwrite whoever actually last edited this.
                updated_by = ad_buy.updated_by
                # Don't call document cloud
                ad_buy.ignore_post_save=True
                ad_buy.save(updated_by)

        unset_adv_buys = PoliticalBuy.objects.filter(advertiser__isnull=False, advertiser_display_name__isnull=True)
        for ad_buy in unset_adv_buys:
            
            ad_buy.advertiser_display_name = adv.advertiser.name
            updated_by = ad_buy.updated_by
            # Don't call document cloud
            ad_buy.ignore_post_save=True
            ad_buy.save(updated_by)
            
        missing_callsigns = PoliticalBuy.objects.filter(broadcaster_callsign__isnull=True)
        for ad_buy in missing_callsigns:
            related_broadcasters = ad_buy.broadcasters.all()
            if len(related_broadcasters) > 0:
                bdcallsign = related_broadcasters[0].callsign
                
                ad_buy.broadcaster_callsign = bdcallsign
                updated_by = ad_buy.updated_by
                # Don't call document cloud
                ad_buy.ignore_post_save=True
                ad_buy.save(updated_by)
                
            
            
        
        
        #uncategorized_ad_buys = PoliticalBuy.objects.filter(advertiser__isnull=False, is_FCC_doc=False)

            
            