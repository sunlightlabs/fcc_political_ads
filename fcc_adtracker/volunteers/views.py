from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.localflavor.us.forms import USStateSelect
from django.contrib.auth.models import User

from registration.views import register

from volunteers.models import Profile
from volunteers.forms import RegistrationFormUniqueEmail, SocialProfileForm, NonUserProfileForm

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

import urllib
import urllib2

try:
    import simplejson as json
except ImportError:
    import json

from smtplib import SMTPException

SIGNUP_EMAIL_REPLY_TO = getattr(settings, 'SIGNUP_EMAIL_REPLY_TO', 'admin@localhost')


def noaccount_signup(request):
    # bsd_url = 'http://bsd.sunlightfoundation.com/page/s/fcc-public-files'
    success_message = 'Thank you for signing up to be a Political Ad Sleuth!'
    if request.method == 'POST':
        form = NonUserProfileForm(request.POST)
        if form.is_valid():
            profile_obj = form.save()

            if profile_obj.email:
                # self.bsd_url += "?source=%s" % request.build_absolute_uri()
                # params = { "email": email, "phone": phone,
                #            "firstname": firstname, "lastname": lastname, "custom-1093": station,
                #            "custom-1116": share_checkbox, "state_cd": state, "city": city
                #           }
                # response = urllib2.urlopen(self.bsd_url, urllib.urlencode(params)).read()

                message_text = render_to_string('volunteers/signup_autoresponse.txt')
                email_message = EmailMessage(success_message,
                                             message_text, 'adsleuth-noreply@sunlightfoundation.com', (profile_obj.email,),
                                             headers={'Reply-To': SIGNUP_EMAIL_REPLY_TO})
                try:
                    email_message.send()
                except SMTPException as e:
                    if hasattr(e, 'message'):
                        logger.error('SMTPException: ' + e.message)
                    else:
                        logger.error('SMTPException error!')

            request.session['nonuser_profile'] = form.cleaned_data

            if request.is_ajax():
                content_str = render_to_string('volunteers/_nonuser_postsignup_message.html', {'profile': profile_obj})
                resp = {'message': success_message, 'content': content_str}
                return HttpResponse(json.dumps(resp), content_type='application/json')

            messages.success(request, success_message)
            referrer = request.META.get('HTTP_REFERER', None)
            return HttpResponseRedirect(referrer or '/')
    else:
        form = NonUserProfileForm()

    if request.is_ajax():
        form_html = render_to_string('volunteers/_nonuser_profile_form.html', {'form': form})
        resp = {'message': 'Error filling out form', 'content': form_html}
        return HttpResponse(json.dumps(resp), content_type='application/json')
    return render(request, 'volunteers/nonuser_profile_edit.html', {'form': form})


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
    if 'nonuser_profile' in request.session:
        nonuser_profile = request.session['nonuser_profile']
    else:
        nonuser_profile = {}
    prerendered_select = USStateSelect(attrs={'required': 'required', 'id': 'state'}).render('state', nonuser_profile.get('state', ''))
    resp = register(request, backend='registration.backends.default.DefaultBackend',
                    form_class=RegistrationFormUniqueEmail, extra_context={'nonuser_profile': nonuser_profile, 'prerendered_select': prerendered_select})

    if request.method == 'POST':

        try:

            user = User.objects.get(username=request.POST['username'])
            user.get_profile()

        except User.DoesNotExist:
            pass

        except Profile.DoesNotExist:

            profile = Profile(
                user=user,
                phone=request.POST.get('phone', ''),
                state=request.POST.get('state', ''),
                zipcode=request.POST.get('zipcode', ''),
                is_a=request.POST.get('is_a', ''),
            )
            profile.save()

    return resp


def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/account/login/')
    try:
        profile = request.user.get_profile()
    except Profile.DoesNotExist:
        profile = None
    return render(request, 'volunteers/profile.html', {'profile': profile})


def account_landing(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/account/login/')

    return HttpResponseRedirect('/account/profile/')
    # return render(request, 'volunteers/account')
