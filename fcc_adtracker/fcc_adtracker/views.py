from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.localflavor.us import us_states
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.conf import settings

from broadcasters.models import Broadcaster
from volunteers.forms import NonUserProfileForm
from volunteers.models import Profile
from fccpublicfiles.models import PoliticalBuy, PoliticalSpot, Organization
from fccpublicfiles.forms import PrelimDocumentForm

from reversion.models import Revision, Version

FEATURED_ADVERTISER_IDS = getattr(settings, 'FEATURED_ADVERTISER_IDS', ())


def home_view(request):
    featured_advertiser_list = Organization.objects.filter(organization_type='AD', id__in=FEATURED_ADVERTISER_IDS)
    resp_obj = {
        'form': NonUserProfileForm,
        'featured_advertiser_list': featured_advertiser_list,
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
        broadcaster_list = Broadcaster.objects.filter(community_state=profile.state)
    except Profile.DoesNotExist:
        profile = broadcaster_list = None

    user_revisions = Revision.objects.filter(user=request.user)
    user_versions = Version.objects.filter(revision_id__in=user_revisions)
    pbuy_type = ContentType.objects.get_for_model(PoliticalBuy)
    pspot_type = ContentType.objects.get_for_model(PoliticalSpot)
    politicalspot_version_list = user_versions.filter(content_type=pspot_type) \
                            .distinct('object_id')
    politicalspot_ids = [vers.object_id for vers in politicalspot_version_list]
    politicalbuy_version_list = user_versions.filter(content_type=pbuy_type) \
                            .distinct('object_id')
    politicalbuy_ids = [vers.object_id for vers in politicalbuy_version_list]
    politicalbuy_list = PoliticalBuy.objects.filter(Q(id__in=politicalbuy_ids) |\
                        Q(politicalspot__in=politicalspot_ids)).distinct().order_by('-updated_at')

    form = PrelimDocumentForm()

    resp_obj = {
        'profile': profile,
        'broadcaster_list': broadcaster_list,
        'politicalbuy_list': politicalbuy_list,
        'form': form,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, 'dashboards/user_dashboard.html', resp_obj)


