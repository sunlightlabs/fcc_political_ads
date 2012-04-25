from django import forms
from mongotools.forms import MongoForm, fields
from .models import Broadcaster, Address


class BroadcasterForm(MongoForm):
    """Form for Broadcaster mongoengine model"""
    callsign = fields.MongoCharField(widget=forms.TextInput(attrs={'readonly':True}))
    network_affiliate = fields.MongoCharField(widget=forms.TextInput(attrs={'readonly':True}))
    
    class Meta:
        document = Broadcaster
        fields = ('callsign', 'network_affiliate')
        
    def __unicode__(self):
        return u"BroadcasterForm"


class AddressForm(MongoForm):
    """Form for Address mongoengine model"""
    title = fields.MongoCharField(widget=forms.TextInput(attrs={'readonly':True}))
    
    class Meta:
        document = Address
        fields = ('title', 'address1', 'address2', 'city', 'state', 'zip1', 'zip2')

    def __unicode__(self):
        return u"AddressForm"