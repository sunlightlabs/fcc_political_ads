from django.shortcuts import render
from django.http import Http404, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us import us_states
from django.conf import settings



from broadcasters.models import Broadcaster, BroadcasterAddress
from broadcasters.json_views import _make_broadcasteraddress_dict
from broadcasters.broadcaster_utils import annotate_broadcaster_queryset
from fccpublicfiles.models import PoliticalBuy

try:
    import simplejson as json
except ImportError:
    import json

STATES_DICT = dict(us_states.US_STATES)
FEATURED_BROADCASTER_STATE = getattr(settings, 'FEATURED_BROADCASTER_STATE', 'OH')

STATES_GEOCENTERS_JSON_FILE = getattr(settings, 'STATES_GEOCENTERS_JSON_FILE', None)
states_geocenters = None
if STATES_GEOCENTERS_JSON_FILE:
    try:
        states_geocenters = json.load(open(STATES_GEOCENTERS_JSON_FILE, 'r'))
    except IOError, e:
        pass

    
def state_broadcaster_list(request, state_id, template_name='broadcasters/broadcaster_table.html'):
    state_id = state_id.upper()
    state_name = STATES_DICT.get(state_id, None)
    state_geocenter = states_geocenters.get(state_id, None) if states_geocenters else None
    if state_name:
        # Want to grab broadcasters with/without addresses, then the addresses themselves...
        ## We're no longer displaying these addresses on this page, so don't bother...
        #broadcaster_list = Broadcaster.objects.filter(community_state=state_id).prefetch_related('broadcasteraddress_set')
        # instead grab the list and annotate it
        broadcaster_list = annotate_broadcaster_queryset(Broadcaster.objects.filter(community_state=state_id))
        
        
        max_documents_to_show = 5
        state_ad_buys = PoliticalBuy.objects.filter(broadcasters__community_state=state_id).order_by('documentcloud_doc__created_at')[:max_documents_to_show]
        
        
        return render(request, template_name, {'broadcaster_list': broadcaster_list, 'state_name': state_name, 'state_geocenter': state_geocenter, 'state_ad_buys':state_ad_buys})
    else:
        raise Http404('State with abbrevation "{state_id}" not found.'.format(state_id=state_id))


def broadcaster_detail(request, callsign, template_name='broadcasters/broadcaster_detail.html'):
    if not callsign.isupper():
        return HttpResponsePermanentRedirect(reverse('broadcaster_politicalbuys_view', kwargs={'callsign':callsign.upper()}))
    try:
        obj = BroadcasterAddress.objects.get(broadcaster__callsign=callsign.upper(), label__name__iexact='studio')
        state_geocenter = states_geocenters.get(obj.broadcaster.community_state, None) if states_geocenters else None
        obj_json = json.dumps(_make_broadcasteraddress_dict(obj))
    except BroadcasterAddress.DoesNotExist:
        try:
            broadcaster = Broadcaster.objects.get(callsign=callsign.upper())
        except Broadcaster.DoesNotExist:
            raise Http404('Broadcaster with callsign "{callsign}" not found.'.format(callsign=callsign))
        obj = {
            'broadcaster': broadcaster,
        }
        state_geocenter = states_geocenters.get(obj['broadcaster'].community_state, None) if states_geocenters else None
        obj_json = None
    return render(request, template_name, {'obj': obj, 'obj_json': obj_json, 'state_geocenter': state_geocenter})


def featured_broadcasters(request, template_name='broadcasters/broadcasters_featured.html'):
    """Featured page. For pilot, perhaps other uses in future."""
    state_name = STATES_DICT.get(FEATURED_BROADCASTER_STATE.upper(), None)
    broadcaster_list = Broadcaster.objects.filter(community_state=FEATURED_BROADCASTER_STATE.upper())
    resp_obj = {
        'broadcaster_list': broadcaster_list,
        'state_name': state_name,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, template_name, resp_obj)
