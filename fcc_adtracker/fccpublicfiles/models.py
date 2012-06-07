from django.db import models
from django.contrib.localflavor.us.models import USStateField

from doccloud.models import Document
from broadcasters.models import get_callsigns
import datetime
import timedelta
from weekday_field import fields as wf_fields

CALLSIGNS = [(c,c) for c in get_callsigns()]

ORGANIZATION_TYPES = (
    (u'MB' ,u'MediaBuyer'),
    (u'AD', u'Advertiser'),
)


class PublicDocument(models.Model):
    station = models.CharField(choices=CALLSIGNS, max_length=12, verbose_name="Station Callsign")
    documentcloud_doc = models.ForeignKey(Document)
    
    def __unicode__(self):
        if self.documentcloud_doc:
            return u"{0}: {1}".format(self.station, self.documentcloud_doc)
        return u"PublicDocument"


class Address(models.Model):
    address1 = models.CharField(blank=True, null=True, max_length=100)
    address2 = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(max_length=50)
    state = USStateField()
    zipcode = models.CharField(blank=True, null=True, max_length=10)

    def __unicode__(self):
        if not self.address1 or self.address1 == '':
            return u"Address"
        return u"Address: " + self.address1


class Person(models.Model):
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "People"
        ordering = ('last_name', 'first_name',)
    
    def __unicode__(self):
        return u"{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)


class Role(models.Model):
    person = models.ForeignKey('Person')
    organization = models.ForeignKey('Organization')
    title = models.CharField(max_length=100, help_text="Job title or descriptor for position they hold.")
    
    def __unicode__(self):
        return u"<" + self.person.__unicode__() + ": " + self.title + " >"


class Organization(models.Model):
    name = models.CharField(max_length=100)
    organization_type = models.CharField(blank=True, max_length=2, choices=ORGANIZATION_TYPES)
    addresses = models.ManyToManyField(Address, blank=True, null=True)
    employees = models.ManyToManyField(Person, through=Role)
    fec_id = models.CharField(max_length=9, blank=True)
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        if self.name:
            return self.name
        return u"Organization"


class PoliticalBuy(PublicDocument):
    """A subset of PublicFile, the PoliticalBuy records purchases of air time (generally for political ads)"""
    contract_number = models.CharField(blank=True, max_length=100)
    advertiser = models.ForeignKey('Organization', blank=True, null=True, related_name='advertiser_politicalbuys', limit_choices_to={'organization_type' : u'AD'})
    advertiser_signatory = models.ForeignKey('Person', blank=True, null=True)
    bought_by = models.ForeignKey('Organization', blank=True, null=True, related_name='mediabuyer_politicalbuys', limit_choices_to={'organization_type' : u'MB'})
    contract_start_date = models.DateField(blank=True, null=True, default=datetime.datetime.today)
    contract_end_date = models.DateField(blank=True, null=True, default=datetime.datetime.today)
    lowest_unit_price = models.NullBooleanField(default=None, blank=True, null=True)


class PoliticalSpot(models.Model):
    """Information particular to a political ad spot (e.g., a candidate ad)"""
    document = models.ForeignKey(PoliticalBuy, verbose_name="Political Buy")
    airing_start_date = models.DateField(blank=True, null=True)
    airing_end_date = models.DateField(blank=True, null=True)
    airing_days = wf_fields.WeekdayField(blank=True)
    timeslot_begin = models.TimeField(blank=True, null=True)
    timeslot_end = models.TimeField(blank=True, null=True)
    show_name = models.CharField(blank=True, max_length=100)
    broadcast_length = timedelta.TimedeltaField(blank=True, null=True, help_text="The easiest way to enter time is as <em>XX minutes, YY seconds</em> or <em>YY seconds</em>.")
    num_spots = models.IntegerField(blank=True, null=True, verbose_name="Number of Spots")
    rate = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text="Dollar cost for each spot")
    preemptable = models.NullBooleanField(default=None, blank=True, null=True)
    
    def documentcloud_doc():
        doc = "The documentcloud_doc property."
        def fget(self):
            if self.document:
                return self.document.documentcloud_doc
            return None
        return locals()
    documentcloud_doc = property(**documentcloud_doc())