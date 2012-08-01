from django.shortcuts import render
from django.contrib.localflavor.us import us_states


def home_view(request):
    resp_obj = {
        'states_dict': us_states.US_STATES,
        'sfapp_base_template': 'sfapp/base-full.html'
    }
    return render(request, 'home.html', resp_obj)