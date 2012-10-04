from fccpublicfiles.models import PoliticalBuy, PoliticalSpot
from django.db.models import Sum, Count

def sum_broadcaster_spent(broadcaster):
    # PoliticalBuy's can be spent on multiple stations (though most aren't); this will attribute all spending on all stations towards each station, giving a wrong answer.
    amount = PoliticalBuy.objects.filter(broadcasters__pk=broadcaster.pk).aggregate(broadcaster_dollars=Sum('total_spent_raw'))
    if amount['broadcaster_dollars']:
        return amount['broadcaster_dollars']
    else:
        return 0

def sum_broadcaster_buys(broadcaster):
    # Will only count the spots that have been entered
    buys = PoliticalBuy.objects.filter(broadcasters__pk=broadcaster.pk).aggregate(total_buys=Count(''))
    if buys['total_buys']:
        #print "%s political buys: %s" % (broadcaster, buys['total_buys'])
        return buys['total_buys']
    else:
        return 0

def annotate_broadcaster_queryset(broadcaster_queryset):
    # Attach number of ads and total amount spent to a queryset of broadcasters.
    # Helper for state_broadcaster_list and wherever else broadcaster-wide numbers are needed.
    for broadcaster in broadcaster_queryset:
        broadcaster.total_spent = sum_broadcaster_spent(broadcaster)
        broadcaster.total_buys = sum_broadcaster_buys(broadcaster)
    return broadcaster_queryset