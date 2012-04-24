from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.defaultfilters import floatformat
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseBadRequest, Http404
from django.core.urlresolvers import reverse
from django.core import serializers

from .models import *
from fcc_adtracker.settings import mongo_conn

from mongoengine import *
from bson.son import SON
from mongo_utils.serializer import encode_model 
try:
    import simplejson as json
except ImportError, e:
    import json


def state_broadcaster_list(request, state_id):
    state_name = STATES_DICT.get(state_id.upper(), None)
    if state_name:
        broadcaster_list = Broadcaster.objects.filter(community_state=state_id.upper())
        return render_to_response('broadcasters/broadcaster_list.html', {'broadcaster_list': broadcaster_list, 'state_name': state_name}, context_instance=RequestContext(request))
    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


def broadcaster_detail(request, callsign):
    if not callsign.isupper():
        return HttpResponsePermanentRedirect(reverse('broadcaster_detail', kwargs={'callsign': callsign.upper()}))
    broadcaster = Broadcaster.objects.get(callsign=callsign.upper())
    if broadcaster:
        return render_to_response('broadcasters/broadcaster_detail.html', {'broadcaster': broadcaster}, context_instance=RequestContext(request))
    else:
        raise Http404('Broadcaster with "{callsign}" not found.'.format(callsign=callsign))
    
    
def nearest_broadcasters_list(request):
    radius = int(request.GET['radius']) if 'radius' in request.GET else 20
    radian_dist = radius/EARTH_RADIUS_MILES
    if 'lat' in request.GET and 'lon' in request.GET:
        lat = float(request.GET['lat'])
        lon = float(request.GET['lon'])
        cursor = mongo_conn.fccads.command(SON([ ('geoNear', 'broadcaster'), ('near', [lon, lat]), ('spherical', True), ('maxDistance', radian_dist) ]))
        results = []
        for item in cursor['results']:
            item['obj']['distance'] = item['dis'] * EARTH_RADIUS_MILES
            del(item['dis'])
            results.append(item['obj'])
        jsonout = json.dumps(results, default=encode_model)
        return HttpResponse(jsonout, content_type='application/javascript')
    else:
        return HttpResponseBadRequest('You must include lat, lon args')