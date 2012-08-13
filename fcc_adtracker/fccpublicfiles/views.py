from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us import us_states
from django.conf import settings

from .models import PoliticalBuy, PoliticalSpot, Broadcaster, Address, AddressLabel

from geopy import distance

STATES_DICT = dict(us_states.US_STATES)
FEATURED_BROADCASTER_STATE = getattr(settings, 'FEATURED_BROADCASTER_STATE', 'OH')


def state_broadcaster_list(request, state_id):
    state_name = STATES_DICT.get(state_id.upper(), None)
    if state_name:
        broadcaster_list = Broadcaster.objects.filter(community_state=state_id.upper())
        return render(request, 'fccpublicfiles/broadcaster_list.html', {'broadcaster_list': broadcaster_list, 'state_name': state_name})
    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


def broadcaster_detail(request, callsign):
    if not callsign.isupper():
        return HttpResponsePermanentRedirect(reverse('broadcaster_detail', kwargs={'callsign': callsign.upper()}))
    broadcaster = Broadcaster.objects.get(callsign=callsign.upper())
    if broadcaster:
        return render(request, 'fccpublicfiles/broadcaster_detail.html', {'broadcaster': broadcaster})
    else:
        raise Http404('Broadcaster with "{callsign}" not found.'.format(callsign=callsign))


def featured_broadcasters(request):
    """Featured page. For pilot, perhaps other uses in future."""
    state_name = STATES_DICT.get(FEATURED_BROADCASTER_STATE.upper(), None)
    broadcaster_list = Broadcaster.objects.filter(community_state=FEATURED_BROADCASTER_STATE.upper())
    resp_obj = {
        'broadcaster_list': broadcaster_list,
        'state_name': state_name,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, 'fccpublicfiles/broadcasters_featured.html', resp_obj)


def nearest_broadcasters_list(request):
    radius = int(request.GET['radius']) if 'radius' in request.GET else 20
    radian_dist = radius/EARTH_RADIUS_MILES
    if 'lat' in request.GET and 'lon' in request.GET:
        lat = float(request.GET['lat'])
        lon = float(request.GET['lon'])
        # cursor = mongo_conn.fccads.command(SON([ ('geoNear', 'broadcaster'), ('near', [lon, lat]), ('spherical', True), ('maxDistance', radian_dist) ]))
        results = []
        for item in cursor['results']:
            item['obj']['distance'] = item['dis'] * EARTH_RADIUS_MILES
            del(item['dis'])
            results.append(item['obj'])
        jsonout = json.dumps(results, default=encode_model)
        return HttpResponse(jsonout, content_type='application/javascript')
    else:
        return HttpResponseBadRequest('You must include lat, lon args')
