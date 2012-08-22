from django.http import HttpResponseRedirect
from .models import Profile


def account_details(request, user=None, *args, **kwargs):

    if 'account_profile' not in request.session and user is None:
        return HttpResponseRedirect('/account/setup-profile/')


def set_account_details(request, user=None, *args, **kwargs):
    if user:
        return {'username': user.username}

    if 'account_profile' in request.session:

        settings = request.session['account_profile']

        details = kwargs.get('details')
        details['email'] = settings['email']
        details['username'] = settings['username']

        return {'username': details['username'], 'email': details['email']}


def create_profile(request, user=None, *args, **kwargs):

    settings = request.session.get('account_profile')

    if settings is not None and user is not None:

        try:

            user.get_profile()

        except Profile.DoesNotExist:

            profile = Profile(
                user=user,
                phone=settings['phone'],
                state=settings['state'],
                is_a=settings['is_a']
            )
            profile.save()


def cleanup(request, user=None, *args, **kwargs):

    if 'account_profile' in request.session:
        del request.session['account_profile']
