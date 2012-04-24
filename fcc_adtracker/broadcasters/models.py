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
    title = StringField()
    address1 = StringField()
    address2 = StringField()
    city = StringField()
    state = StringField()
    zip1 = StringField()
    zip2 = StringField()
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
    callsign = StringField(unique=True)
    network_affiliate = StringField()
    facility_type = StringField()
    community_city = StringField()
    community_state = StringField(max_length=2, choices=us_states.US_STATES)
    
    def as_json(self):
        return json.dumps(self, default=encode_model)
    
    meta = {'allow_inheritance': False}
    
    def __unicode__(self):
        return u"Broadcaster"

