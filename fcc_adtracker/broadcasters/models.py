from __future__ import division
from django.contrib.localflavor.us import us_states

from mongoengine import *
from mongo_utils.serializer import encode_model 
try:
    import simplejson as json
except ImportError, e:
    import json



STATES_DICT = dict(us_states.US_STATES)

EARTH_RADIUS_MILES = float(3959)


class Address(EmbeddedDocument):
    """Postal Address"""
    title = StringField(max_length=80)
    address1 = StringField(max_length=40)
    address2 = StringField(max_length=40)
    city = StringField(max_length=20)
    state = StringField(max_length=2, choices=us_states.US_STATES)
    zip1 = StringField(max_length=5)
    zip2 = StringField(max_length=4)
    pos = ListField()

    def as_json(self):
        return json.dumps(self, default=encode_model)
    
    meta = {
        'allow_inheritance': False,
        'indexes': [ '*pos', ],
    }
    
    def __unicode__(self):
        return u"Address"


class Broadcaster(DynamicDocument):
    """Broadcaster, based on FCC's CDBS facility table"""
    addresses = ListField(EmbeddedDocumentField(Address))
    callsign = StringField(max_length=12, unique=True)
    channel = IntField()
    nielsen_dma = StringField(max_length=60)
    network_affiliate = StringField(max_length=100)
    facility_type = StringField(max_length=3)
    community_city = StringField(max_length=20)
    community_state = StringField(max_length=2, choices=us_states.US_STATES)
    
    def as_json(self):
        return json.dumps(self, default=encode_model)
    
    meta = {'allow_inheritance': False}
    
    def __unicode__(self):
        return u"Broadcaster"



def get_callsigns():
    return [b.callsign for b in Broadcaster.objects.only('callsign').all().order_by('callsign')]

