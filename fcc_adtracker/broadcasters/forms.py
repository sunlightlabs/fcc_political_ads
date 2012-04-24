from django import forms
from mongotools.forms import MongoForm, fields
from .models import Broadcaster, Address

class BroadcasterForm(MongoForm):
    """Form for Broadcaster mongoengine model"""
    callsign = fields.MongoCharField()
    network_affiliate = fields.MongoCharField()
    community_city = fields.MongoCharField()
    community_state = fields.MongoCharField()
    # facility_type = fields.MongoCharField(editable=False)
    
    class Meta:
        document = Broadcaster
        exclude = ('facility_type',)
        
    def __unicode__(self):
        return u"BroadcasterForm"


class AddressForm(MongoForm):
    """Form for Address mongoengine model"""

    class Meta:
        document = Address
        fields = ('title', 'address1', 'address2', 'city', 'state', 'zip1', 'zip2')

    def __unicode__(self):
        return u"AddressForm"