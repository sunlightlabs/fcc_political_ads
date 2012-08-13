from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from registration.views import register

from mongoengine import *

from .models import *
from .forms import RegistrationProfileUniqueEmail, SocialProfileForm

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


import urllib
import urllib2

from smtplib import SMTPException

SIGNUP_EMAIL_REPLY_TO = getattr(settings, 'SIGNUP_EMAIL_REPLY_TO', 'admin@localhost')


class ActionSignupView(View):

    bsd_url = 'http://bsd.sunlightfoundation.com/page/s/fcc-public-files'
    success_message = 'Thanks for registering!'

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(('POST',))

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        firstname = request.POST.get("firstname", "")
        lastname = request.POST.get("lastname", "")
        station = request.POST.get("custom-1093", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state_cd", "")
        share_checkbox = request.POST.get("custom-1116", "")

        signup = Signup(email=email, phone=phone, firstname=firstname, lastname=lastname, city=city, state=state, broadcaster=station)
        # try:
        #     broadcaster = Broadcaster.objects.get(callsign=station)
        #     signup.broadcaster = broadcaster
        # except Broadcaster.DoesNotExist as e:
        #     pass
        signup.share_checkbox = share_checkbox or False
        try:
            signup.save()
        except ValidationError as e:
            return HttpResponse(json.dumps(e.to_dict()), content_type='application/json')

        if email:
            self.bsd_url += "?source=%s" % request.build_absolute_uri()
            params = { "email": email, "phone": phone,
                       "firstname": firstname, "lastname": lastname, "custom-1093": station,
                       "custom-1116": share_checkbox, "state_cd": state, "city": city
                      }
            response = urllib2.urlopen(self.bsd_url, urllib.urlencode(params)).read()

        message_text = render_to_string('volunteers/signup_autoresponse.txt')
        email_message = EmailMessage('Thank you for signing up to be a Political Ad Sleuth!',
                                     message_text, 'adsleuth-noreply@sunlightfoundation.com', (email,),
                                     headers={'Reply-To': SIGNUP_EMAIL_REPLY_TO})
        try:
            email_message.send()
        except SMTPException as e:
            if hasattr(e, 'message'):
                logger.error('SMTPException: ' + e.message)
            else:
                logger.error('SMTPException error!')

        if request.is_ajax():
            resp = {'message': self.success_message}
            return HttpResponse(json.dumps(resp), content_type='application/json')

        messages.success(request, self.success_message)
        referrer = request.META.get('HTTP_REFERER', None)

        return HttpResponseRedirect(referrer or '/')


def setup_profile(request):
    if 'partial_pipeline' not in request.session:
        return HttpResponseRedirect('/')

    pipeline = request.session['partial_pipeline']

    if request.method == 'POST':

        form = SocialProfileForm(request.POST)

        if form.is_valid():

            request.session['account_profile'] = form.cleaned_data

            return redirect('socialauth_complete', backend=pipeline['backend'])

    else:
        form = SocialProfileForm(initial=pipeline['kwargs']['details'])

    return render(request, 'volunteers/profile_setup.html', {'form': form})


def register_volunteer(request, *args, **kwargs):
    resp = register(request, backend='registration.backends.default.DefaultBackend', form_class=RegistrationProfileUniqueEmail)

    if request.method == 'POST':

        try:

            user = User.objects.get(username=request.POST['username'])
            user.get_profile()

        except User.DoesNotExist:
            pass

        except Profile.DoesNotExist:

            data = request.POST

            profile = Profile(
                user=user,
                phone=data.get('phone', ''),
                state=data.get('state', ''),
                is_a=data.get('is_a', ''),
            )
            profile.save()

    return resp


def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/account/login/')
    try:
        profile = request.user.get_profile()
    except Profile.DoesNotExist as e:
        profile = None
    return render(request, 'volunteers/profile.html', {'profile': profile})


def account_landing(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/account/login/')

    return HttpResponseRedirect('/account/profile/')
    # return render(request, 'volunteers/account')
