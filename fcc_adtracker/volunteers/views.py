from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotAllowed, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.exceptions import ObjectDoesNotExist

from registration.views import register

from mongoengine import *
from bson.son import SON

from .models import *
from .forms import RegistrationProfileUniqueEmail

try:
    import simplejson as json
except ImportError, e:
    import json

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
        share_checkbox = request.POST.get("custom-1116", "")

        signup = Signup( email=email, phone=phone, firstname=firstname, lastname=lastname )
        try:
            broadcaster = Broadcaster.objects.get(callsign=station)
            signup.broadcaster = broadcaster
        except Broadcaster.DoesNotExist as e:
            pass
        signup.share_checkbox = share_checkbox or False
        try:
            signup.save()
        except ValidationError as e:
            return HttpResponse(json.dumps(e.to_dict()), content_type='application/json')

        if email:
            self.bsd_url += "?source=%s" % request.build_absolute_uri()
            params = {"email": email, "phone": phone, "firstname": firstname, "lastname": lastname, "custom-1093": station, "custom-1116": share_checkbox}
            response = urllib2.urlopen(self.bsd_url, urllib.urlencode(params)).read()


        message_text = render_to_string('volunteers/signup_autoresponse.txt')
        email_message = EmailMessage( 'Thank you for signing up to be a Political Ad Sleuth in Wisconsin!',
                                    message_text, 'adsleuth-noreply@sunlightfoundation.com', (email,),
                                    headers={'Reply-To':SIGNUP_EMAIL_REPLY_TO} )
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


def register_volunteer(request, *args, **kwargs):
    resp = register(request,
                backend='registration.backends.default.DefaultBackend',
                form_class=RegistrationProfileUniqueEmail)


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
    except Profile.DoesNotExist, SiteProfileNotAvailable:
        profile = None
    return render(request, 'volunteers/profile.html', {'profile': profile})

