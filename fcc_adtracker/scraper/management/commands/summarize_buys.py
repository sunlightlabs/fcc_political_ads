import datetime
import pytz
utc=pytz.UTC


from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum, Count
from django.contrib.localflavor.us import us_states
from scraper.models import *

STATES_DICT = dict(us_states.US_STATES)



today = datetime.datetime.now()
one_week_ago = today - datetime.timedelta(days=7)
one_week_ago = utc.localize(one_week_ago)


def summarize_ads(this_obj_summary, all_ads):

    # sigh. 
    total_buys = 0
    pres_buys = 0
    outside_buys = 0
    sen_buys = 0
    house_buys = 0
    state_buys = 0
    local_buys = 0
    recent_pres_buys = 0
    recent_sen_buys = 0
    recent_house_buys = 0
    recent_outside_buys = 0

    for ad in all_ads:
        total_buys += 1
        time = ad.upload_time
        adtype = ad.candidate_type()
    
        if adtype == 'Non-Candidate Issue Ads':
            outside_buys += 1
            if time >= one_week_ago:
                recent_outside_buys += 1
    
        elif adtype == 'President':
            pres_buys += 1
            if time >= one_week_ago:
                recent_pres_buys += 1        
        
        elif adtype == 'US Senate':
            sen_buys += 1
            if time >= one_week_ago:
                recent_sen_buys += 1    

        elif adtype == 'US House':
            house_buys += 1
            if time >= one_week_ago:
                recent_house_buys += 1  

        elif adtype == 'State':
            state_buys += 1
        
        elif adtype == 'Local':
            local_buys += 1

    this_obj_summary.tot_buys = total_buys 
    this_obj_summary.pres_buys = pres_buys
    this_obj_summary.outside_buys = outside_buys
    this_obj_summary.sen_buys = sen_buys
    this_obj_summary.house_buys = house_buys
    this_obj_summary.house_buys = state_buys
    this_obj_summary.local_buys = local_buys
    this_obj_summary.state_buys = state_buys
    this_obj_summary.recent_pres_buys = recent_pres_buys
    this_obj_summary.recent_sen_buys = recent_sen_buys
    this_obj_summary.recent_house_buys = recent_house_buys
    this_obj_summary.recent_outside_buys = recent_outside_buys 
    this_obj_summary.save()


class Command(BaseCommand):
    help = "Create summaries at state, DMA level"
    requires_model_validation = False


    def handle(self, *args, **options):
        mandated_broadcasters = StationData.objects.filter(is_mandated_station=True)
        
        states = mandated_broadcasters.values('communityState').annotate(count=Count('pk')).order_by('communityState')
        for state in states:
            state_id = state['communityState']
            print "state %s" % state_id
            (this_state_summary, created) = state_summary.objects.get_or_create(state_id=state_id)
            this_state_summary.num_broadcasters = state['count']
            all_ads = PDF_File.objects.filter(community_state=state_id)
            
            summarize_ads(this_state_summary, all_ads)
        
        dmas = mandated_broadcasters.values('nielsenDma_id').annotate(count=Count('pk'))
        #print dmas
        for dma in dmas:
            print "dma %s" % dma
            dma_id = dma['nielsenDma_id']
            (this_dma_summary, created) = dma_summary.objects.get_or_create(dma_id=dma_id)
            this_dma_summary.num_broadcasters = dma['count']
            all_ads = PDF_File.objects.filter(dma_id=dma_id)
            
            summarize_ads(this_dma_summary, all_ads)
            
           
            