from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
from django.contrib.localflavor.us import us_states

try:
    import simplejson as json
except ImportError, e:
    import json


IS_A_CHOICES = (
    ('other', 'Other'),
    ('journalist', 'Journalist'),
    ('researcher', 'Researcher'),
    ('activist', 'Activist'),
    ('student', 'Student'),
    ('nonprofit', 'Non-profit'),
)


class BaseProfile(models.Model):
    phone = PhoneNumberField(blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = USStateField(choices=us_states.US_STATES, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    is_a = models.CharField(max_length=16, choices=IS_A_CHOICES, blank=True)
    share_info = models.BooleanField(default=True)

    class Meta:
        abstract = True
        permissions = (
            ('view_unshared_profile', 'Can view unshared profiles'),
        )

    def __unicode__(self):
        return u'<{0}: {1}, {2}>'.format(self.id, self.city, self.state)


class NonUserProfile(BaseProfile):
    '''
        For people who want to sign up but not create an account.
    '''
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'))
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return u'NonUserProfile: ' + self.email

# User model records first_name, last_name, and email...


class Profile(BaseProfile):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'Profile: ' + self.user.username
