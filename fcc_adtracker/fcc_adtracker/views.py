from django.shortcuts import render
from django.contrib.localflavor.us import us_states
from volunteers.forms import NonUserProfileForm


def home_view(request):
    resp_obj = {
        'form': NonUserProfileForm,
        'states_dict': us_states.US_STATES,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, 'home.html', resp_obj)