from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
from django.contrib.localflavor.us import us_states

from mongoengine import *
from mongo_utils.serializer import encode_model
import datetime

try:
    import simplejson as json
except ImportError, e:
    import json

# from broadcasters.models import Broadcaster


IS_A_CHOICES = (
    ('other', 'Other'),
    ('journalist', 'Journalist'),
    ('researcher', 'Researcher'),
    ('activist', 'Activist'),
    ('student', 'Student'),
    ('nonprofit', 'Non-profit'),
)

# Signup model was used for pilot. Fields may be indicators of additional fields needed on Profile, or new model(?)
class Signup(Document):
    email = EmailField()
    phone = StringField()
    firstname = StringField()
    lastname = StringField()
    state = StringField()
    city = StringField()
    # broadcaster = ReferenceField('Broadcaster')
    broadcaster = StringField()
    _share_info = BooleanField(default=False)
    date_submitted = DateTimeField(default=datetime.datetime.now)

    def share_checkbox():
        doc = "The share_checkbox property."
        def fget(self):
            return self._share_info
        def fset(self, value):
            self._share_info = True if value == "on" else False
        def fdel(self):
            del self._share_info
        return locals()
    share_checkbox = property(**share_checkbox())

# Signup.register_delete_rule(Broadcaster, 'bar', NULLIFY)


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone = PhoneNumberField(blank=True, null=True)
    state = USStateField(blank=True, null=True)
    is_a = models.CharField(max_length=16, choices=IS_A_CHOICES, blank=True)

    def __unicode__(self):
        return u'Profile: ' + self.user.username

