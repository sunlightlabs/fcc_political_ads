import datetime
import csv

from django.http import Http404
from django.shortcuts import render_to_response, redirect

from models import StationData, PDF_File, dma_summary, state_summary
from fccpublicfiles.models import PoliticalBuy
from broadcasters.models import Broadcaster
from django.db.models import Count
from django.contrib.localflavor.us import us_states

from django.conf import settings
from django.views.decorators.cache import cache_page
CSV_EXPORT_DIR = getattr(settings, 'CSV_EXPORT_DIR', 'csv_exports')


STATES_DICT = dict(us_states.US_STATES)
CACHE_TIME = 15 * 60


@cache_page(CACHE_TIME)
def state_fcc_list(request):

    states = state_summary.objects.filter(tot_buys__gte=0).order_by('-tot_buys')

    return render_to_response('geography_list.html', {
        'geography_name': 'state',
        'geography_name_short': 'state',
        'geography_list': states,
        'sfapp_base_template': 'sfapp/base-full.html',

    })


@cache_page(CACHE_TIME)
def recent_state_fcc_list(request):

    states = state_summary.objects.filter(tot_buys__gte=0).order_by('-tot_buys')

    return render_to_response('recent_geography_list.html', {
        'geography_name': ' state',
        'geography_name_short': 'state',
        'geography_list': states,
        'sfapp_base_template': 'sfapp/base-full.html',

    })


@cache_page(CACHE_TIME)
def dma_fcc_list(request):

    dmas = dma_summary.objects.filter(tot_buys__gte=0).order_by('-tot_buys')
    return render_to_response('geography_list.html', {
        'geography_name': 'TV market',
        'geography_name_short': 'dma',
        'geography_list': dmas,
        'sfapp_base_template': 'sfapp/base-full.html',
    })


@cache_page(CACHE_TIME)
def recent_dma_fcc_list(request):

    dmas = dma_summary.objects.filter(tot_buys__gte=0).order_by('-tot_buys')
    return render_to_response('recent_geography_list.html', {
        'geography_name': 'TV market',
        'geography_name_short': 'dma',
        'geography_list': dmas,
        'sfapp_base_template': 'sfapp/base-full.html',
    })


@cache_page(CACHE_TIME)
def station_fcc_list(request):

    broadcasters = StationData.objects.filter(is_mandated_station=True).order_by('callSign').values('callSign', 'networkAfil', 'communityCity', 'communityState', 'nielsenDma')

    for broadcaster in broadcasters:
        broadcaster['geography_name'] = "%s (%s)" % (broadcaster['callSign'], broadcaster['networkAfil'])
        broadcaster['geography_name_short'] = broadcaster['callSign']
        broadcaster['location1'] = "%s, %s" % (broadcaster['communityCity'], broadcaster['communityState'])
        broadcaster['location2'] = broadcaster['nielsenDma']
    return render_to_response('broadcaster_list.html', {
        'geography_name': 'TV station',
        'geography_name_short': 'tv-station',
        'geography_list': broadcasters,
        'show_location': 'True',
    })


@cache_page(CACHE_TIME)
def station_state_list(request, state_id):
    state_name = STATES_DICT.get(state_id, None)
    if state_name:
        broadcasters = StationData.objects.filter(is_mandated_station=True, communityState=state_id).order_by('callSign').values('callSign', 'networkAfil', 'communityCity', 'communityState', 'nielsenDma')

        for broadcaster in broadcasters:
            broadcaster['geography_name'] = "%s (%s)" % (broadcaster['callSign'], broadcaster['networkAfil'])
            broadcaster['geography_name_short'] = broadcaster['callSign']
            broadcaster['location1'] = "%s" % (broadcaster['communityCity'])
            broadcaster['location2'] = broadcaster['nielsenDma']
        return render_to_response('broadcaster_list.html', {
            'geography_name': 'TV station',
            'geography_name_short': 'tv-station',
            'geography_list': broadcasters,
            'show_location': 'True',
            'subgeography': state_name,
        })

    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


@cache_page(CACHE_TIME)
def station_dma_list(request, dma_id):
    dma_name = None

    broadcasters = StationData.objects.filter(is_mandated_station=True, nielsenDma_id=dma_id).order_by('callSign').values('callSign', 'networkAfil', 'communityCity', 'communityState', 'nielsenDma')

    for broadcaster in broadcasters:
        if not dma_name:
            dma_name = broadcaster['nielsenDma']

        broadcaster['geography_name'] = "%s (%s)" % (broadcaster['callSign'], broadcaster['networkAfil'])
        broadcaster['geography_name_short'] = broadcaster['callSign']
        broadcaster['location1'] = "%s, %s" % (broadcaster['communityCity'], broadcaster['communityState'])
        broadcaster['location2'] = broadcaster['nielsenDma']
    return render_to_response('broadcaster_list.html', {
        'geography_name': 'TV station',
        'geography_name_short': 'tv-station',
        'geography_list': broadcasters,
        'show_location': 'True',
        'subgeography': dma_name,
    })


@cache_page(CACHE_TIME)
def filing_dma_list(request, dma_id):
    dma_name = None

    filings = PDF_File.objects.filter(dma_id=dma_id).order_by('-upload_time')
    count = filings.aggregate(numfilings=Count('pk'))['numfilings']
    if filings:
        dma_name = filings[0].folder.broadcaster.nielsen_dma
    return render_to_response('filing_list.html', {
        'filings': filings,
        'geography_name': dma_name,
        'preposition': 'in',
        'count': count,
        'sfapp_base_template': 'sfapp/base-full.html',
    })


@cache_page(CACHE_TIME)
def filing_station_list(request, callsign):

    filings = PDF_File.objects.filter(callsign__iexact=callsign).order_by('-upload_time')
    count = filings.aggregate(numfilings=Count('pk'))['numfilings']
    broadcaster = None
    try:
        broadcaster = Broadcaster.objects.get(callsign=callsign)
    except Broadcaster.DoesNotExist:
        pass

    return render_to_response('filing_list.html', {
        'filings': filings,
        'geography_name': callsign,
        'preposition': 'from',
        'count': count,
        'broadcaster': broadcaster,
        'sfapp_base_template': 'sfapp/base-full.html',

    })


@cache_page(CACHE_TIME)
def filing_state_list(request, state_id):
    state_name = STATES_DICT.get(state_id, None)
    if state_name:

        filings = PDF_File.objects.filter(community_state=state_id).order_by('-upload_time')
        count = filings.aggregate(numfilings=Count('pk'))['numfilings']

        return render_to_response('filing_list.html', {
            'filings': filings,
            'geography_name': state_name,
            'preposition': 'in',
            'count': count,
            'sfapp_base_template': 'sfapp/base-full.html',
        })

    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


@cache_page(CACHE_TIME)
def fcc_most_recent(request):

    today = datetime.datetime.today()
    one_week_ago = today - datetime.timedelta(days=7)

    filings = PDF_File.objects.filter(upload_time__gte=one_week_ago).order_by('-upload_time')
    count = filings.aggregate(numfilings=Count('pk'))['numfilings']

    return render_to_response('filing_list.html', {
        'filings': filings,
        'geography_name': 'the last week',
        'preposition': 'in',
        'count': count,
        'sfapp_base_template': 'sfapp/base-full.html',
    })


def ad_buy_redirect(request, buy_id):
    adbuy = PoliticalBuy.objects.get(related_FCC_file__pk=buy_id)
    return redirect(adbuy.get_absolute_url())
