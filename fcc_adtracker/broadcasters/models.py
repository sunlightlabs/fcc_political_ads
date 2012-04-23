from __future__ import division
from django.contrib.localflavor.us import us_states

from mongoengine import *
from mongo_utils.serializer import encode_model 
try:
    import simplejson as json
except ImportError, e:
    import json


POSITION = {
    'type': 'array',
    "minItems": 2,
    "maxItems": 3
}

ADDRESS = {
    'type': 'object',
    'properties': {
        "address1": {'type': 'string'}, 
        "address2": {'type': 'string', 'required': False},                 
        "state": {'type': 'string'}, 
        "city": {'type': 'string'}, 
        "zip": {'type': 'string'}, 
        "zip2": {'type': 'string', 'required': False},
        "pos": POSITION
    }
}

BROADCASTER = {
    'type': 'object',
    'properties': {
        "addresses": {
            'type': 'object',
            'properties': {
                "fcc": { 'type': ADDRESS },
                "studio": { 'type': ADDRESS }        
            }
        },
        "network_affiliate": {'type': 'string', 'required': False}, 
        "facility_type": {'type': 'string', 'required': False}, 
        "callsign": {'type': 'string', 'required': True}, 
        "community_city": {'type': 'string', 'required': False}, 
        "community_state": {'type': 'string', 'required': True}    
    }
}

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



def get_broadcaster_by_callsign(callsign):
    broadcasters = db.fccads.broadcasters
    return broadcasters.find_one({'callsign': callsign})
    

def get_broadcasters_for_state(state):
    broadcasters = db.fccads.broadcasters
    cursor =  broadcasters.find({'community_state': state}).sort('callsign')
    return [x for x in cursor]


def nearby_broadcaster_stations(lat, lon, radius=50):
    lat = float(lat)
    lon = float(lon)
    
    radian_dist = radius/EARTH_RADIUS_MILES
    
    cursor = db.fccads.command(SON([ ('geoNear', 'broadcasters'), ('near', [lon, lat]), ('spherical', True), ('maxDistance', radian_dist) ]))
    
    results = []
    for item in cursor['results']:
        item['distance'] = item['dis'] * EARTH_RADIUS_MILES
        results.append(item)
    return results