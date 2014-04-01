from optparse import make_option
from datetime import date,timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum, Count

from scraper.models import PDF_File, dma_summary, dma_weekly


cycle_iso_start = date(2012,12,31)

def get_week_number(thedate):
    """ helper function that returns the week number for the 2014 cycle """
    (year, week, day) = thedate.isocalendar()
    return (52*(year-2013)) + week

def get_week_end(week_number):
    # last sunday of the week
    return (cycle_iso_start + timedelta(days=(week_number)*7-1))

def get_week_start(week_number):
    # first monday of the week
    return (cycle_iso_start + timedelta(days=(week_number-1)*7))


def summarize_week(week_number):
    week_start = get_week_start(week_number)
    week_end = get_week_end(week_number)

    # Only summarize top 50 districts
    for dma in dma_summary.objects.filter(num_broadcasters__gte=1):

        dma_id = dma.dma_id
        
        # sigh. 
        total_buys = 0
        pres_buys = 0
        outside_buys = 0
        sen_buys = 0
        house_buys = 0
        state_buys = 0
        local_buys = 0
        
        all_ads = PDF_File.objects.filter(dma_id=dma_id, upload_time__gte=week_start, upload_time__lte=week_end)
        for ad in all_ads:
            total_buys += 1
            time = ad.upload_time
            adtype = ad.ad_type

            if adtype == 'Non-Candidate Issue Ads':
                outside_buys += 1

            elif adtype == 'President':
                pres_buys += 1        

            elif adtype == 'US Senate':
                sen_buys += 1
                
            elif adtype == 'US House':
                house_buys += 1

            elif adtype == 'State':
                state_buys += 1

            elif adtype == 'Local':
                local_buys += 1

        (this_obj_summary, created) = dma_weekly.objects.get_or_create(dma_id=dma_id, cycle_week_number=week_number, defaults={'dma_name': dma.dma_name, 'fcc_dma_name':dma.fcc_dma_name})
        this_obj_summary.tot_buys = total_buys 
        this_obj_summary.pres_buys = pres_buys
        this_obj_summary.outside_buys = outside_buys
        this_obj_summary.sen_buys = sen_buys
        this_obj_summary.house_buys = house_buys
        this_obj_summary.local_buys = local_buys
        this_obj_summary.state_buys = state_buys
        this_obj_summary.save()
        


class Command(BaseCommand):
    help = """Set weekly ad activity by dma. 
            By default just calculates the current week. 
            Use the --all option to calculate all weeks."""
    requires_model_validation = False

    option_list = BaseCommand.option_list + (
            make_option('--all',
                action='store_true',
                dest='run_all',
                default=False,
                help='Summarize all weeks, not just the current one'),
            )

    def handle(self, *args, **options):
        current_week_number = get_week_number(date.today())
        week_list = [current_week_number]
        if options['run_all']:
            week_list = range(1,current_week_number+1)

        for week_number in week_list:
            print "Summarizing week %s" % (week_number)
            summarize_week(week_number)
