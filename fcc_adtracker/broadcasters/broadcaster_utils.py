from fccpublicfiles.models import PoliticalBuy, PoliticalSpot
from django.db.models import Sum

def sum_broadcaster_spent(broadcaster):
    # PoliticalBuy's can be spent on multiple stations (though most aren't); this will attribute all spending on all stations towards each station, giving a wrong answer.
    amount = PoliticalBuy.objects.filter(broadcasters__pk=broadcaster.pk).aggregate(broadcaster_dollars=Sum('total_spent_raw'))
    if amount['broadcaster_dollars']:
        return amount['broadcaster_dollars']
    else:
        return 0

def sum_broadcaster_spots(broadcaster):
    # Will only count the spots that have been entered
    spots = PoliticalSpot.objects.filter(document__broadcasters__pk=broadcaster.pk).aggregate(total_spots=Sum('num_spots'))
    if spots['total_spots']:
        return spots['total_spots']
    else:
        return 0
    
def annotate_broadcaster_queryset(broadcaster_queryset):
    # Attach number of ads and total amount spent to a queryset of broadcasters. 
    # Helper for state_broadcaster_list and wherever else broadcaster-wide numbers are needed. 
    for broadcaster in broadcaster_queryset:
        broadcaster.total_spent = sum_broadcaster_spent(broadcaster)
        broadcaster.total_spots = sum_broadcaster_spots(broadcaster)
    return broadcaster_queryset