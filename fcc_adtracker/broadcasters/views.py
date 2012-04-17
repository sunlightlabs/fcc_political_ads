from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseBadRequest, Http404

from .models import get_broadcasters_for_state, nearby_broadcaster_stations, STATES_DICT

import json
from bson import json_util

def state_broadcaster_list(request, state_id):
    state_name = STATES_DICT.get(state_id.upper(), None)
    if state_name:
        broadcaster_list = get_broadcasters_for_state(state_id.upper())
        return render_to_response('broadcasters/broadcaster_list.html', {'broadcaster_list': broadcaster_list, 'state_name': state_name}, context_instance=RequestContext(request))
    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


def nearest_broadcasters_list(request):
    radius = int(request.GET['radius']) if 'radius' in request.GET else 20
    
    if 'lat' in request.GET and 'lon' in request.GET:
        
        locations = nearby_broadcaster_stations(request.GET['lat'], request.GET['lon'], radius=radius)
        
        return HttpResponse(json.dumps(locations, default=json_util.default, indent=4), content_type='application/javascript')
    else:
        return HttpResponseBadRequest('You must include lat, lon args')