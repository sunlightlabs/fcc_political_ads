from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.localflavor.us.forms import USStateSelect
from django.contrib.auth.models import User
# from django.contrib.auth.views import logout

from registration.views import register

from volunteers.models import Profile
from volunteers.forms import BetterRegistrationFormUniqueEmail, UserProfileForm, AccountProfileForm, NonUserProfileForm

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

try:
    import simplejson as json
except ImportError:
    import json

from smtplib import SMTPException

SIGNUP_EMAIL_REPLY_TO = getattr(settings, 'SIGNUP_EMAIL_REPLY_TO', 'admin@localhost')
SIGNUP_EXTRA_FIELDS = getattr(settings, 'SIGNUP_EXTRA_FIELDS', None)


def noaccount_signup(request):
    """ Initial signup that gets us user info but does not create an account."""
    success_message = 'Thank you for signing up to be a Political Ad Sleuth!'
    if request.method == 'POST':
        form = NonUserProfileForm(request.POST)
        if form.is_valid():
            profile_obj = form.save()
            if SIGNUP_EXTRA_FIELDS:
                extra_field_data = {}
                for extra_field in SIGNUP_EXTRA_FIELDS:
                    if extra_field in request.POST:
                        extra_field_data[extra_field] = request.POST.getlist(extra_field)
                profile_obj.extra_fields = extra_field_data
                profile_obj.save()
            if profile_obj.email:

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
            request.session['nonuser_profile']['extra_fields'] = profile_obj.extra_fields
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
    """Part of social_auth pipeline."""
    if 'partial_pipeline' not in request.session:
        return HttpResponseRedirect('/')

    pipeline = request.session['partial_pipeline']
    if request.method == 'POST':

        form = UserProfileForm(request.POST)

        if form.is_valid():

            request.session['account_profile'] = form.cleaned_data

            return redirect('socialauth_complete', backend=pipeline['backend'])

    else:
        if 'nonuser_profile' in request.session:
            initial_data = request.session['nonuser_profile'].copy()
            cleaned_details = dict([(k, v) for k, v in pipeline['kwargs']['details'].iteritems() if v != ''])
            initial_data.update(cleaned_details)
        else:
            initial_data = pipeline['kwargs']['details']
        form = UserProfileForm(initial=initial_data)

    return render(request, 'volunteers/profile_setup.html', {'form': form})


@login_required
def view_profile(request):
    try:
        profile = request.user.get_profile()
    except Profile.DoesNotExist:
        profile = None
    return render(request, 'volunteers/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    """Edit an existing profile"""
    user = request.user
    if request.method == 'POST':
        form = AccountProfileForm(request.POST)
        if form.is_valid():
            still_valid = True

            qs = User.objects.exclude(pk=user.pk)

            if qs.filter(email=form.cleaned_data['email']).exists():
                form.errors['email'] = ['Email address has been used by another account']
                still_valid = False

            if qs.filter(username=form.cleaned_data['username']).exists():
                form.errors['username'] = ['Username has been used by another account']
                still_valid = False

            if still_valid:

                # update password
                has_usable_pw = user.has_usable_password()

                new_pw = form.cleaned_data.get('new_password')
                new_pw_confirm = form.cleaned_data.get('new_password_confirm')

                if new_pw and has_usable_pw:
                    old_pw = form.cleaned_data.get('old_password')

                    if not user.check_password(old_pw):
                        form.errors['old_password'] = ['You did not enter your old password correctly']
                        still_valid = False
                    else:
                        if new_pw_confirm:
                            if new_pw == new_pw_confirm:
                                user.set_password(form.cleaned_data['new_password'])
                            else:
                                form.errors['new_password'] = ['Password and confirmation did not match.']
                                still_valid = False
                        else:
                            form.errors['new_password_confirm'] = ['Please confirm your new password.']
                            still_valid = False
                elif new_pw:
                    if new_pw_confirm:
                        if new_pw == new_pw_confirm:
                            user.set_password(form.cleaned_data['new_password'])
                        else:
                            form.errors['new_password'] = ['Password and confirmation did not match.']
                            still_valid = False
                    else:
                        form.errors['new_password_confirm'] = ['Please confirm your new password.']
                        still_valid = False

            if still_valid:

                # set user attributes

                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']

                user.save()

                # set profile attributes

                profile = Profile.objects.get_or_create(user=user)[0]

                profile.phone = form.cleaned_data['phone']
                profile.city = form.cleaned_data['city']
                profile.state = form.cleaned_data['state']
                profile.zipcode = form.cleaned_data['zipcode']
                profile.is_a = form.cleaned_data['is_a']
                profile.notify = form.cleaned_data['notify']

                profile.save()

                messages.success(request, 'Your account has been updated.')

                return redirect('account_landing')
    else:
        initial_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        try:
            profile = request.user.get_profile()
            initial_data['phone'] = profile.phone
            initial_data['city'] = profile.city
            initial_data['state'] = profile.state
            initial_data['zipcode'] = profile.zipcode
            initial_data['is_a'] = profile.is_a
            initial_data['share_info'] = profile.share_info
            initial_data['notify'] = profile.notify
        except Profile.DoesNotExist:
            profile = None
        form = AccountProfileForm(initial=initial_data)
    return render(request, 'volunteers/profile_edit.html', {'form': form})


def register_volunteer(request, *args, **kwargs):
    """Override of default django-registration register, adding
    NonUserProfile data to profile
    """
    if 'nonuser_profile' in request.session:
        nonuser_profile = request.session['nonuser_profile']
    else:
        nonuser_profile = {}
    prerendered_select = USStateSelect(attrs={'required': 'required', 'id': 'state'}).render('state', nonuser_profile.get('state', ''))
    resp = register(request, backend='registration.backends.default.DefaultBackend',
                    form_class=BetterRegistrationFormUniqueEmail, extra_context={'nonuser_profile': nonuser_profile, 'prerendered_select': prerendered_select})

    if request.method == 'POST':

        try:

            user = User.objects.get(username=request.POST['username'])
            user.first_name = nonuser_profile.get('first_name', request.POST.get('first_name', ''))
            user.last_name = nonuser_profile.get('last_name', request.POST.get('last_name', ''))
            user.save()
            user.get_profile()

        except User.DoesNotExist:
            pass

        except Profile.DoesNotExist:
            profile = Profile(
                user=user,
                phone=nonuser_profile.get('phone', request.POST.get('phone', '')),
                city=nonuser_profile.get('city', request.POST.get('city', '')),
                state=nonuser_profile.get('state', request.POST.get('state', '')),
                zipcode=nonuser_profile.get('zipcode', request.POST.get('zipcode', '')),
                is_a=nonuser_profile.get('is_a', request.POST.get('is_a', ''))
            )
            profile.save()

    return resp


# def delete_account(request):

#     if request.user.is_staff:
#         messages.warning(request,
#             'Unable to delete account. Staff accounts must be deleted by an administrator.')
#         return HttpResponseRedirect('/account/')

#     if request.method == 'POST':

#         if 'iamreallysure' in request.POST:

#             user = request.user
#             resp = logout(request, next_page='/')
#             user.delete()

#             return resp

#     return render(request, 'volunteers/account_delete.html')

def account_error(request):
    """For account errors. social_auth requires this in their config."""
    return render(request, 'volunteers/account_error.html',)


@login_required
def account_landing(request):
    return HttpResponseRedirect('/account/profile/')
