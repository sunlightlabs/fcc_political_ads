from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.defaultfilters import floatformat
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseBadRequest, Http404
from django.core.urlresolvers import reverse
from django.core import serializers

from .models import *

import json
from bson import json_util

def clean_output_objects(input_list):
    cleaned_objs = []
    for inny in input_list:
        if inny.get('_id'):
            del inny['_id']
        cleaned_objs.append(inny)
    return cleaned_objs

def generate_broadcaster_html(broadcaster):
    return render_to_string('broadcasters/_broadcaster_snippet.html',  {'broadcaster': broadcaster})


def state_broadcaster_list(request, state_id):
    state_name = STATES_DICT.get(state_id.upper(), None)
    if state_name:
        broadcaster_list = get_broadcasters_for_state(state_id.upper())
        for broadcaster in broadcaster_list:
            broadcaster['html'] = generate_broadcaster_html(broadcaster)
        jsonout = json.dumps(clean_output_objects(broadcaster_list), default=json_util.default, indent=4)
        return render_to_response('broadcasters/broadcaster_list.html', {'broadcaster_list': broadcaster_list, 'state_name': state_name, 'broadcaster_json': jsonout}, context_instance=RequestContext(request))
    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


def broadcaster_detail(request, callsign):
    if not callsign.isupper():
        return HttpResponsePermanentRedirect(reverse('broadcaster_detail', kwargs={'callsign': callsign.upper()}))
    broadcaster = get_broadcaster_by_callsign(callsign.upper())
    if broadcaster:
        return render_to_response('broadcasters/_broadcaster_snippet.html', {'broadcaster': broadcaster}, context_instance=RequestContext(request))
    else:
        raise Http404('Broadcaster with "{callsign}" not found.'.format(callsign=callsign))
    
    
def nearest_broadcasters_list(request):
    radius = int(request.GET['radius']) if 'radius' in request.GET else 20
    
    if 'lat' in request.GET and 'lon' in request.GET:
        
        locations = nearby_broadcaster_stations(request.GET['lat'], request.GET['lon'], radius=radius)
        
        output = []
        for loc in locations:
            obj = loc.get('obj');
            obj['distance'] = floatformat(loc.get('distance'), 2)
            obj['html'] = generate_broadcaster_html(obj)
            output.append(obj)
        jsonout = json.dumps(clean_output_objects(output), default=json_util.default, indent=4)
        return HttpResponse(jsonout, content_type='application/javascript')
    else:
        return HttpResponseBadRequest('You must include lat, lon args')