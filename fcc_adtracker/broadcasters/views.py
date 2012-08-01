from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import View
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.defaultfilters import floatformat
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseBadRequest, Http404
from django.contrib.localflavor.us import us_states
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core import serializers
from django.conf import settings

from .models import *
from .forms import *
from fcc_adtracker.settings import mongo_conn

from mongoengine import *
from bson.son import SON
from mongo_utils.serializer import encode_model
from mongotools.views import (CreateView, UpdateView,
                              DeleteView, ListView,
                              DetailView)
try:
    import simplejson as json
except ImportError, e:
    import json

import urllib
import urllib2


FEATURED_BROADCASTER_STATE = getattr(settings, 'FEATURED_BROADCASTER_STATE', 'OH')


def state_broadcaster_list(request, state_id):
    state_name = STATES_DICT.get(state_id.upper(), None)
    if state_name:
        broadcaster_list = Broadcaster.objects.filter(community_state=state_id.upper())
        return render(request, 'broadcasters/broadcaster_list.html', {'broadcaster_list': broadcaster_list, 'state_name': state_name})
    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


def broadcaster_detail(request, callsign):
    if not callsign.isupper():
        return HttpResponsePermanentRedirect(reverse('broadcaster_detail', kwargs={'callsign': callsign.upper()}))
    broadcaster = Broadcaster.objects.get(callsign=callsign.upper())
    if broadcaster:
        return render(request, 'broadcasters/broadcaster_detail.html', {'broadcaster': broadcaster})
    else:
        raise Http404('Broadcaster with "{callsign}" not found.'.format(callsign=callsign))


def featured_broadcasters(request):
    """Featured page. For pilot, perhaps other uses in future."""
    state_name = STATES_DICT.get(FEATURED_BROADCASTER_STATE.upper(), None)
    broadcaster_list = Broadcaster.objects.filter(community_state=FEATURED_BROADCASTER_STATE.upper(), addresses__title='studio', addresses__pos__exists=True)
    resp_obj = {
        'broadcaster_list': broadcaster_list,
        'state_name': state_name,
        'states_dict': us_states.US_STATES,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, 'broadcasters/broadcasters_featured.html', resp_obj)


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


def edit_broadcaster(request, callsign):
    """For getting form for updating broadcaster"""
    broadcaster = Broadcaster.objects.get(callsign=callsign.upper())
    if broadcaster:
        address_forms = []
        bform = BroadcasterForm(instance=broadcaster)
        for address in broadcaster.addresses:
            address_forms.append(AddressForm(instance=address))
        resp_obj = {
            'broadcaster': broadcaster,
            'broadcaster_form': bform,
            'address_forms': address_forms
        }
        return render(request, 'broadcasters/broadcaster_change_form.html', resp_obj)
    else:
        raise Http404('Broadcaster with "{callsign}" not found.'.format(callsign=callsign))



