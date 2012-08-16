from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us import us_states
from django.conf import settings
from django.core import serializers

from .models import PoliticalBuy, PoliticalSpot, Broadcaster, Address, BroadcasterAddress, AddressLabel

from geopy import distance
from geopy.point import Point

import os.path
try:
    import simplejson as json
except ImportError:
    import json

import copy

STATES_DICT = dict(us_states.US_STATES)
FEATURED_BROADCASTER_STATE = getattr(settings, 'FEATURED_BROADCASTER_STATE', 'OH')

STATES_GEOCENTERS_JSON_FILE = getattr(settings, 'STATES_GEOCENTERS_JSON_FILE', None)
if STATES_GEOCENTERS_JSON_FILE:
    try:
        states_geocenters = json.load(open(STATES_GEOCENTERS_JSON_FILE, 'r'))
    except IOError, e:
        states_geocenters = None

def _make_broadcasteraddress_dict(bc_ad_obj):
    '''
    Transform a BroadcasterAddress into a dictionary that can be modified and serialized to json
    '''
    obj_dict = {
                'broadcaster': dict(copy.copy(bc_ad_obj.broadcaster.__dict__)),
                'combined_address': bc_ad_obj.address.combined_address,
                'address': dict(copy.copy(bc_ad_obj.address.__dict__))
            }
    obj_dict['broadcaster'].pop('id')
    obj_dict['broadcaster'].pop('_state')
    obj_dict['address'].pop('id')
    obj_dict['address'].pop('_state')
    obj_dict['address']['label'] = bc_ad_obj.label.name
    return obj_dict


def state_broadcaster_list(request, state_id):
    state_id = state_id.upper()
    state_name = STATES_DICT.get(state_id, None)
    if states_geocenters:
        state_geocenter = states_geocenters.get(state_id, None)
    else:
        state_geocenter = None
    if state_name:
        # Want to grab broadcasters with/without addresses, then the addresses themselves...
        broadcaster_list = Broadcaster.objects.filter(community_state=state_id).prefetch_related('broadcasteraddress_set')
        return render(request, 'fccpublicfiles/broadcaster_list.html', {'broadcaster_list': broadcaster_list, 'state_name': state_name, 'state_geocenter': state_geocenter})
    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


def broadcaster_detail(request, callsign):
    if not callsign.isupper():
        return HttpResponsePermanentRedirect(reverse('broadcaster_detail', kwargs={'callsign': callsign.upper()}))
    try:
        obj = BroadcasterAddress.objects.get(broadcaster__callsign=callsign.upper(), label__name__iexact='studio')
        obj_json = json.dumps(_make_broadcasteraddress_dict(obj))
        return render(request, 'fccpublicfiles/broadcaster_detail.html', {'obj': obj, 'obj_json': obj_json})
    except BroadcasterAddress.DoesNotExist:
        try:
            broadcaster = Broadcaster.objects.get(callsign=callsign.upper())
            obj = {
                'broadcaster': broadcaster,
            }
            obj_json = None
            return render(request, 'fccpublicfiles/broadcaster_detail.html', {'obj': obj, 'obj_json': obj_json})
        except Broadcaster.DoesNotExist:
            raise Http404('Broadcaster with callsign "{callsign}" not found.'.format(callsign=callsign))


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


def state_broadcaster_addresses(request, state_id, label_slug):
    state_id = state_id.upper()
    state_name = STATES_DICT.get(state_id, None)

    if state_name is None:
        return HttpResponseNotFound(json.dumps({'error': 'No state found for "{0}"'.format(state_id)}), content_type='application/json')
    if label_slug == 'all':
        label_list = AddressLabel.objects.all()
    else:
        try:
            label_list = [AddressLabel.objects.get(slug=label_slug)]
        except AddressLabel.DoesNotExist:
            return HttpResponseNotFound(json.dumps({'error': '{0} is not in the list of address labels.'.format(label_slug)}), content_type='application/json')

    state_broadcaster_list = BroadcasterAddress.objects.filter(label__in=label_list, broadcaster__community_state=state_id).distinct()
    if len(state_broadcaster_list) == 0:
        return HttpResponseNotFound(json.dumps({'error': 'No broadcaster addresses labeled "{0}" in {1}'.format(label_slug, state_name)}), content_type='application/json')
    obj_list = []
    for obj in state_broadcaster_list:
        obj_dict = _make_broadcasteraddress_dict(obj)
        obj_list.append(obj_dict)
    jsonout = json.dumps(obj_list)
    return HttpResponse(jsonout, content_type='application/json')


def nearest_broadcasters_list(request):
    radius = int(request.GET['radius']) if 'radius' in request.GET else 20
    if 'lat' in request.GET and 'lon' in request.GET:
        lat = float(request.GET['lat'])
        lng = float(request.GET['lon'])
        search_point = Point(lat, lng)

        # a degree of latitude is between 68.703 and 69.407 miles
        # a degree of longitude is about 53 miles at the 40th parallel
        # This roughly narrows down the search to 200 miles. I like fudge. Do you?
        max_dist = Point(lat + 2, lng + 2.8)
        min_dist = Point(lat - 2, lng - 2.8)
        nearby_broadcaster_list = BroadcasterAddress.objects.filter(label__name='studio',
                                                                    address__lat__range=(min_dist.latitude,max_dist.latitude),
                                                                    address__lng__range=(min_dist.longitude, max_dist.longitude)).distinct()

        obj_list = []
        for obj in nearby_broadcaster_list:
            pt = Point(obj.address.lat, obj.address.lng)
            miles_away = distance.distance(search_point, pt).miles
            if miles_away < radius:
                obj_dict = _make_broadcasteraddress_dict(obj)
                obj_dict['distance'] = miles_away
                obj_list.append(obj_dict)
        sorted_obj_list = sorted(obj_list, key=lambda x: x['distance'])
        jsonout = json.dumps(sorted_obj_list)
        return HttpResponse(jsonout, content_type='application/json')
    else:
        return HttpResponseBadRequest('You must include lat, lon args')
