import datetime
from operator import itemgetter
    
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.utils.html import escape
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.contrib.localflavor.us import us_states

from doccloud.models import Document

from .models import *
from fccpublicfiles.forms import PrelimDocumentForm, PoliticalBuyFormFull,\
        SimpleOrganizationForm, AdvertiserSignatoryForm, RelatedPoliticalSpotForm

from broadcasters.models import Broadcaster
from django.db.models import Count

from name_cleaver import IndividualNameCleaver


DOCUMENTCLOUD_DEFAULT_ACCESS_LEVEL = getattr(settings, 'DOCUMENTCLOUD_DEFAULT_ACCESS_LEVEL', 'private')
NEEDS_ENTRY_DMAS = getattr(settings, 'NEEDS_ENTRY_DMAS', None)

STATES_DICT = dict(us_states.US_STATES)
CACHE_TIME = 15 * 60


def politicalbuy_view(request, uuid_key, template_name='politicalbuy_view.html', message=None):
    obj = get_object_or_404(PoliticalBuy, uuid_key=uuid_key)
    return render(request, template_name, {'obj': obj, 'message':message})


@login_required
@transaction.commit_on_success
def prelim_doc_form(request, template_name='document_submit.html'):

    form = PrelimDocumentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save(commit=False)
        uploaded_file = request.FILES['file']

        # make the doccloud model
        cloud_doc = Document(
            file=uploaded_file,
            title=uploaded_file.name,
            user=request.user,
            access_level=DOCUMENTCLOUD_DEFAULT_ACCESS_LEVEL
        )
        # upload
        cloud_doc.connect_dc_doc()
        cloud_doc.save()

        pol_buy = PoliticalBuy(
            documentcloud_doc=cloud_doc
        )
        pol_buy.save(request.user)

        pol_buy.broadcasters = form.cleaned_data['broadcasters']
        pol_buy.save(request.user)

        return redirect('politicalbuy_edit', uuid_key=pol_buy.uuid_key)

    return render(request, template_name, {'form': form})


@login_required
def politicalbuy_edit(request, uuid_key, template_name='politicalbuy_edit.html'):
    myobject = get_object_or_404(PoliticalBuy, uuid_key=uuid_key)

    form = PoliticalBuyFormFull(request.POST or None, instance=myobject)
    if form.is_valid():
        print "form is valid"
        myobject = form.save(commit=False)
        myobject.save(request.user)
        # redirect on success. Would be nice to display the message here, but..
        return redirect('politicalbuy_view', uuid_key)
    else:
        print "form is not valid"

    return render(request, template_name, {'form': form, 'obj': myobject, 'sfapp_base_template': 'sfapp/base-full.html'})


@login_required
def handlePopAdd(request, addForm, field, initial_data=None, current_object=None):
    """ Using methods adapted from:
         http://sontek.net/blog/detail/implementing-djangos-admin-interface-pop-ups
         and
         http://www.awebcoder.com/post/16/djangos-admin-related-objects-pop-up-in-the-front-end
    """
    if request.method == "POST":
        form = addForm(request.POST, instance=current_object)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
            except forms.ValidationError:
                obj = None
            if obj:
                obj.save(request.user)
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(obj._get_pk_val()), escape(obj)))
    else:
        if current_object:
            form = addForm(instance=current_object)
        else:
            form = addForm(initial_data)
    pageContext = {'form': form, 'field': field}
    return render(request, 'add_model_view.html', pageContext)


@login_required
def edit_related_politicalspot(request, uuid_key, spot_id=None):
    if spot_id:
        try:
            current_obj = PoliticalSpot.objects.get(id=int(spot_id))
        except PoliticalSpot.DoesNotExist:
            current_obj =  None
    else:
        current_obj =  None
    initial_data = {
        'document': PoliticalBuy.objects.get(uuid_key=uuid_key)
    }
    if current_obj:
        initial_data['id'] = current_obj.id

    return handlePopAdd(request, RelatedPoliticalSpotForm, 'politicalspot', initial_data=initial_data, current_object=current_obj)


@login_required
def add_advertiser(request):
    org_defaults = {'organization_type': 'AD'}
    if 'search' in request.GET:
        org_defaults['name'] = request.GET['search']
    return handlePopAdd(request, SimpleOrganizationForm, 'advertiser', initial_data=org_defaults)


@login_required
def add_media_buyer(request):
    org_defaults = {'organization_type': 'MB'}
    if 'search' in request.GET:
        org_defaults['name'] = request.GET['search']
    return handlePopAdd(request, SimpleOrganizationForm, 'mediabuyer', initial_data=org_defaults)


@login_required
def add_advertiser_signatory(request):
    if 'advertiser_id' in request.GET:
        defaults = {
            'advertiser_id': request.GET['advertiser_id'] or None
        }
    else:
        defaults = {}
    if 'search' in request.GET:
        input_name = IndividualNameCleaver(request.GET['search']).parse(safe=True)
        if isinstance(input_name, basestring):
            defaults['first_name'] = input_name
        else:
            defaults['first_name'] = input_name.first
            defaults['middle_name'] = input_name.middle
            defaults['last_name'] = input_name.last
            defaults['suffix'] = input_name.suffix

    if request.method == "POST":
        form = AdvertiserSignatoryForm(request.POST)
        if form.is_valid():
            person = Person()
            person.first_name = form.data['first_name']
            person.middle_name = form.data.get('middle_name', None)
            person.last_name = form.data['last_name']
            person.suffix = form.data.get('suffix', None)
            person.save(request.user)
            if 'advertiser_id' in form.data:
                adv_id = form.data.get('advertiser_id', None)
                if adv_id:
                    try:
                        advertiser = Organization.objects.get(id=adv_id)
                        role = Role(person=person, organization=advertiser)
                        role.title = form.data.get('job_title', '')
                        role.save(request.user)
                    except Organization.DoesNotExist:
                        # What else to do in this case?
                        pass
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(person._get_pk_val()), escape(person)))
    return handlePopAdd(request, AdvertiserSignatoryForm, 'advertiser_signatory', initial_data=defaults)


def related_spots_ajax(request, uuid_key):
    if request.is_ajax():
        try:
            buy = PoliticalBuy.objects.get(uuid_key=uuid_key)
        except PoliticalBuy.DoesNotExist:
            return HttpResponseNotFound()
        politicalspot_list = buy.politicalspot_set.all()
        pageContext = {
            'politicalspot_list': politicalspot_list,
            'editable': True,
            'uuid_key': uuid_key
        }
        return render(request, '_politicalspots_table.html', pageContext)
    else:
        return HttpResponseBadRequest('<p>Request must be an XMLHttpRequest</p>')

@cache_page(CACHE_TIME)
def state_fcc_list(request):

    states = state_summary.objects.filter(tot_buys__gte=0).order_by('-tot_buys')

    return render(request, 'geography_list.html', {
        'geography_name': 'state',
        'geography_name_short': 'state',
        'geography_list': states,
        'sfapp_base_template': 'sfapp/base-full.html',

    })


@cache_page(CACHE_TIME)
def recent_state_fcc_list(request):

    states = state_summary.objects.filter(tot_buys__gte=0).order_by('-tot_buys')

    return render(request, 'recent_geography_list.html', {
        'geography_name': ' state',
        'geography_name_short': 'state',
        'geography_list': states,
        'sfapp_base_template': 'sfapp/base-full.html',

    })


@cache_page(CACHE_TIME)
def dma_fcc_list(request):

    dmas = dma_summary.objects.filter(tot_buys__gte=0).order_by('-tot_buys')
    return render(request, 'geography_list.html', {
        'geography_name': 'TV market',
        'geography_name_short': 'dma',
        'geography_list': dmas,
        'sfapp_base_template': 'sfapp/base-full.html',
    })


@cache_page(CACHE_TIME)
def recent_dma_fcc_list(request):

    dmas = dma_summary.objects.filter(tot_buys__gte=0).order_by('-tot_buys')
    return render(request, 'recent_geography_list.html', {
        'geography_name': 'TV market',
        'geography_name_short': 'dma',
        'geography_list': dmas,
        'sfapp_base_template': 'sfapp/base-full.html',
    })

"""
@cache_page(CACHE_TIME)
def station_fcc_list(request):

    broadcasters = Broadcaster.objects.all().order_by('callsign').values('callsign', 'networkAfil', 'communityCity', 'communityState', 'nielsenDma')

    for broadcaster in broadcasters:
        broadcaster['geography_name'] = "%s (%s)" % (broadcaster['callsign'], broadcaster['network_affiliate'])
        broadcaster['geography_name_short'] = broadcaster['callsign']
        broadcaster['location1'] = "%s, %s" % (broadcaster['community_city'], broadcaster['community_state'])
        broadcaster['location2'] = broadcaster['nielsenDma']
    return render_to_response('broadcaster_list.html', {
        'geography_name': 'TV station',
        'geography_name_short': 'tv-station',
        'geography_list': broadcasters,
        'show_location': 'True',
    })
"""

@cache_page(CACHE_TIME)
def station_state_list(request, state_id):
    state_name = STATES_DICT.get(state_id, None)
    if state_name:
        broadcasters = Broadcaster.objects.filter(community_state=state_id).order_by('callsign').values('callsign', 'network_affiliate', 'community_city', 'community_state', 'nielsen_dma', 'is_mandated')

        for broadcaster in broadcasters:
            broadcaster['geography_name'] = "%s (%s)" % (broadcaster['callsign'], broadcaster['network_affiliate'])
            broadcaster['geography_name_short'] = broadcaster['callsign']
            broadcaster['location1'] = "%s" % (broadcaster['community_city'])
            broadcaster['location2'] = broadcaster['nielsen_dma']
        return render(request, 'broadcaster_list.html', {
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

    broadcasters = Broadcaster.objects.filter(dma_id=dma_id).order_by('callsign').values('callsign', 'network_affiliate', 'community_city', 'community_state', 'nielsen_dma', 'is_mandated')

    for broadcaster in broadcasters:
        if not dma_name:
            dma_name = broadcaster['nielsen_dma']

        broadcaster['geography_name'] = "%s (%s)" % (broadcaster['callsign'], broadcaster['network_affiliate'])
        broadcaster['geography_name_short'] = broadcaster['callsign']
        broadcaster['location1'] = "%s, %s" % (broadcaster['community_city'], broadcaster['community_state'])
        broadcaster['location2'] = broadcaster['nielsen_dma']
    return render(request, 'broadcaster_list.html', {
        'geography_name': 'TV station',
        'geography_name_short': 'tv-station',
        'geography_list': broadcasters,
        'show_location': 'True',
        'subgeography': dma_name,
    })


@cache_page(CACHE_TIME)
def filing_dma_list(request, dma_id):
    dma_name = None
    dma_summary_found = False
    this_dma_summary = None
    try:
        this_dma_summary = dma_summary.objects.filter(dma_id=dma_id)
        dma_summary_found = True
    except dma_summary.DoesNotExist:
        pass

    filings = PoliticalBuy.objects.filter(dma_id=dma_id).order_by('-upload_time')
    count = filings.aggregate(numfilings=Count('pk'))['numfilings']
    if filings:
        dma_name = filings[0].nielsen_dma
    return render(request, 'filing_list.html', {
        'filings': filings,
        'geography_name': dma_name,
        'preposition': 'in',
        'count': count,
        'sfapp_base_template': 'sfapp/base-full.html',
        'has_summary_data':dma_summary_found,
        'dma_summary':this_dma_summary
    })


@cache_page(CACHE_TIME)
def filing_station_list(request, callsign):

    filings = PoliticalBuy.objects.filter(broadcaster_callsign__iexact=callsign).order_by('-upload_time')
    count = filings.aggregate(numfilings=Count('pk'))['numfilings']
    broadcaster = None
    try:
        broadcaster = Broadcaster.objects.get(callsign=callsign)
    except Broadcaster.DoesNotExist:
        pass

    return render(request, 'filing_list.html', {
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

        filings = PoliticalBuy.objects.filter(community_state=state_id).order_by('-upload_time')
        count = filings.aggregate(numfilings=Count('pk'))['numfilings']

        return render(request, 'filing_list.html', {
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
    three_days_ago = today - datetime.timedelta(days=3)

    filings = PoliticalBuy.objects.filter(upload_time__gte=three_days_ago).order_by('-upload_time')
    count = filings.aggregate(numfilings=Count('pk'))['numfilings']

    return render(request, 'filing_list.html', {
        'filings': filings,
        'geography_name': 'the last three days',
        'preposition': 'in',
        'count': count,
        'sfapp_base_template': 'sfapp/base-full.html',
    })


def needs_entry(self):
    obj = PoliticalBuy.status_objects.get_one_that_needs_entry(dma_id_filter=NEEDS_ENTRY_DMAS)
    return redirect('politicalbuy_edit', uuid_key=obj.uuid_key)

@cache_page(CACHE_TIME)
def advertiser_list(request):
    # only show biggie advertisters that we've explicitly set to display
    advertisers = TV_Advertiser.objects.filter(is_displayed=True)
    
    return render(request, 'advertiser_list.html', {
        'advertisers': advertisers,
        'sfapp_base_template': 'sfapp/base-full.html',
    })
    
@cache_page(CACHE_TIME)
def advertiser_detail(request, advertiser_pk):
    advertiser = get_object_or_404(TV_Advertiser, pk=advertiser_pk)
    today = datetime.datetime.today()
    week_ago = today - datetime.timedelta(days=7)
    advertising_org  = Organization.objects.get(organization_type='AD', related_advertiser=advertiser)
    print advertising_org
    recent_ads = PoliticalBuy.objects.filter(advertiser=advertising_org, contract_start_date__gte=week_ago).order_by('-contract_start_date')
    
    market_summary_raw = recent_ads.values('nielsen_dma', 'dma_id').annotate(market_total=Count('id'))
    

    market_summary = sorted(market_summary_raw, key=itemgetter('market_total'), reverse=True)
    
    top_market_summary = None
    if market_summary:
        top_market_summary = market_summary[0]
    
    return render(request, 'advertiser_detail.html', {
        'advertiser': advertiser,
        'market_summary':market_summary,
        'top_market_summary':top_market_summary,
        'filings':recent_ads,
    })
