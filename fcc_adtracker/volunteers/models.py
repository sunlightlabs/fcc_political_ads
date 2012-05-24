from mongoengine import *
from mongo_utils.serializer import encode_model 
import datetime

try:
    import simplejson as json
except ImportError, e:
    import json

from broadcasters.models import Broadcaster

class Signup(Document):
    email = EmailField()
    phone = StringField()
    firstname = StringField()
    lastname = StringField()
    broadcaster = ReferenceField('Broadcaster')
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

Signup.register_delete_rule(Broadcaster, 'bar', NULLIFY)
    
