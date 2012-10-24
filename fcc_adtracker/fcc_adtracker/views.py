from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.localflavor.us import us_states

from django.conf import settings

from broadcasters.models import Broadcaster
from volunteers.forms import NonUserProfileForm
from volunteers.models import Profile
from fccpublicfiles.models import PoliticalBuy, dma_summary
from fccpublicfiles.forms import PrelimDocumentForm

FEATURED_ADVERTISER_IDS = getattr(settings, 'FEATURED_ADVERTISER_IDS', ())

TOP_THINGS_LIMIT = 10


def home_view(request):
    top_recent_pres_buys = dma_summary.objects.filter(pres_buys__isnull=False).order_by('-pres_buys')[:TOP_THINGS_LIMIT]
    top_recent_outside_buys = dma_summary.objects.filter(recent_outside_buys__isnull=False).order_by('-recent_outside_buys')[:TOP_THINGS_LIMIT]

    resp_obj = {
        'form': NonUserProfileForm,
        'top_recent_pres_buys': top_recent_pres_buys,
        'top_recent_outside_buys': top_recent_outside_buys,
        'states_dict': us_states.US_STATES,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, 'home.html', resp_obj)


@login_required
def user_dashboard(request):
    """Display user details and related information from
        fccpublicfiles and broadcasters apps
    """
    try:
        profile = request.user.get_profile()
        broadcaster_list = Broadcaster.objects.filter(community_state=profile.state, is_mandated=False)
    except Profile.DoesNotExist:
        profile = broadcaster_list = None

    politicalbuy_list = PoliticalBuy.objects.filter(created_by=request.user).order_by('-created_at')

    form = PrelimDocumentForm()

    resp_obj = {
        'profile': profile,
        'broadcaster_list': broadcaster_list,
        'politicalbuy_list': politicalbuy_list,
        'form': form,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, 'dashboards/user_dashboard.html', resp_obj)
