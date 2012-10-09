from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.localflavor.us import us_states
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from locations.models import AddressLabel
from broadcasters.models import Broadcaster, BroadcasterAddress

from geopy import distance
from geopy.point import Point

try:
    import simplejson as json
except ImportError:
    import json

import copy

STATES_DICT = dict(us_states.US_STATES)

BROADCASTER_SERIALIZED_FIELDS = ('channel', 'community_city', 'community_state')

ADDRESS_JSON_FIELDS = (
    'address1',
    'address2',
    'city',
    'state',
    'zipcode',
    'lat',
    'lng',
)


def _sanitize_broadcaster_for_serliazation(broadcaster):
    """docstring for _sanitize_broadcaster_json"""
    bc_dict = dict(copy.copy(broadcaster.__dict__))
    bc_dict.pop('id')
    bc_dict.pop('_state')
    bc_dict['combined_name'] = '{0} [{1} {2}]'.format(broadcaster.callsign, broadcaster.network_affiliate, broadcaster.channel)
    return bc_dict


def _make_broadcasteraddress_dict(bc_ad_obj):
    '''
    Transform a BroadcasterAddress into a dictionary that can be modified and serialized to json
    '''
    obj_dict = {
        'broadcaster': dict(copy.copy(bc_ad_obj.broadcaster.__dict__)),
        'combined_address': bc_ad_obj.address.combined_address,
    }
    obj_dict['broadcaster'].pop('id')
    obj_dict['broadcaster'].pop('_state')
    obj_dict['address'] = dict([(field, bc_ad_obj.address.__dict__[field]) for field in ADDRESS_JSON_FIELDS])
    obj_dict['address']['label'] = bc_ad_obj.label.name
    return obj_dict


# Will probably go away once API implemented.
def state_broadcasters_json(request, state_id):
    state_id = state_id.upper()
    state_name = STATES_DICT.get(state_id, None)
    if state_name:
        state_broadcaster_list = Broadcaster.objects.filter(community_state=state_id).order_by('callsign')
        obj_list = [_sanitize_broadcaster_for_serliazation(bc) for bc in state_broadcaster_list]
        jsonout = json.dumps(obj_list, cls=DjangoJSONEncoder)
        return HttpResponse(jsonout, content_type='application/json')
    else:
        return HttpResponseNotFound(json.dumps({'error': '"{0}" does not match a valid state abbreviation'.format(state_id)}), content_type='application/json')


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
                                                                    address__lat__range=(min_dist.latitude, max_dist.latitude),
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
        jsonout = json.dumps(sorted_obj_list, cls=DjangoJSONEncoder)
        return HttpResponse(jsonout, content_type='application/json')
    else:
        return HttpResponseBadRequest('You must include lat, lon args')


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
    jsonout = json.dumps(obj_list, cls=DjangoJSONEncoder)
    return HttpResponse(jsonout, content_type='application/json')
