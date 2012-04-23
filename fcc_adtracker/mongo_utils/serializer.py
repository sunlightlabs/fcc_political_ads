from mongoengine import *
import mongoengine
from pymongo.objectid import ObjectId
from bson.objectid import ObjectId as BSONObjectId
from types import ModuleType
from itertools import groupby

DB_KEYS = (None, 'id')

def encode_model(obj, ignore_keys=True):
    if isinstance(obj, (mongoengine.Document, mongoengine.EmbeddedDocument)):
        out = dict(obj._data)
        if ignore_keys:
            for dbkey in DB_KEYS:
                if out.get(dbkey, False) is not False:
                    del(out[dbkey])
        for k,v in out.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
    elif isinstance(obj, BSONObjectId):
        out = str(obj)
    elif isinstance(obj, mongoengine.queryset.QuerySet):
        out = list(obj)
    elif isinstance(obj, ModuleType):
        out = None
    elif isinstance(obj, groupby):
        out = [ (g,list(l)) for g,l in obj ]
    elif isinstance(obj, (list,dict)):
        out = obj
    else:
        raise TypeError, "Could not JSON-encode type '%s': %s" % (type(obj), str(obj))
    return out
