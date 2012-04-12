from django.conf import settings
import pymongo

DATA_FIELDS = {
    "broadcaster": [
        "city", 
        "zip", 
        "address1", 
        "address2", 
        "network_affiliate", 
        "facility_type", 
        "state", 
        "callsign", 
        "zip2", 
        "community_city", 
        "community_state"
    ]
    
}



class LazyDatabase(object):

    def __init__(self):
        self._dbs = {}

    def __getattr__(self, attr):

        if attr not in self._dbs:

            host = getattr(settings, 'MONGO_HOST', 'localhost')
            port = getattr(settings, 'MONGO_PORT', 27017)
            name = getattr(settings, 'MONGO_DATABASE', None)

            conn = pymongo.Connection(host, port)
            self._dbs[attr] = conn[name]

        return self._dbs.get(attr, None)

db = LazyDatabase()