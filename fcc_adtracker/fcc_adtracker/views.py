from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us import us_states

from broadcasters.models import Broadcaster

from volunteers.forms import NonUserProfileForm
from volunteers.models import Profile


def home_view(request):
    resp_obj = {
        'form': NonUserProfileForm,
        'states_dict': us_states.US_STATES,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, 'home.html', resp_obj)


def user_dashboard(request):
    """Display user details and related information from
        fccpublicfiles and broadcasters apps
    """
    if request.user.is_authenticated():
        try:
            profile = Profile.objects.get(user=request.user)
            broadcaster_list = Broadcaster.objects.filter(community_state=profile.state)
        except Profile.DoesNotExist:
            profile = broadcaster_list = None
        resp_obj = {
            'profile': profile,
            'broadcaster_list': broadcaster_list
        }
        return render(request,
                'dashboards/user_dashboard.html', resp_obj)
    else:
        return redirect('auth_login')


def account_to_dashboard_landing(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    return HttpResponseRedirect((reverse('user_dashboard')))
