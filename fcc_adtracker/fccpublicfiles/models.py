from django.db import models
from doccloud.models import Document
from broadcasters.models import get_callsigns
import datetime
import timedelta

CALLSIGNS = [(c,c) for c in get_callsigns()]

class PublicDocument(models.Model):
    station = models.CharField(choices=CALLSIGNS, max_length=12, verbose_name="Station Callsign")
    documentcloud_doc = models.ForeignKey(Document)

    def __unicode__(self):
        if self.documentcloud_doc:
            return u"{0}: {1}".format(self.station, self.documentcloud_doc)
        return u"PublicDocument"



class PoliticalBuy(PublicDocument):
    """A subset of PublicFile, the PoliticalBuy records purchases of air time (generally for political ads)"""
    contract_number = models.CharField(blank=True, null=True, max_length=100)
    advertiser = models.CharField(blank=True, null=True, max_length=100)
    ordered_by = models.CharField(blank=True, null=True, max_length=100)
    contract_start_date = models.DateField(blank=True, null=True, default=datetime.datetime.today)
    contract_end_date = models.DateField(blank=True, null=True, default=datetime.datetime.today)



class PoliticalSpot(models.Model):
    """Information particular to a political ad spot (e.g., a candidate ad)"""
    document = models.ForeignKey(PoliticalBuy, verbose_name="Political Buy")
    airing_start_date = models.DateField(blank=True, null=True, default=datetime.datetime.today)
    airing_end_date = models.DateField(blank=True, null=True, default=datetime.datetime.today)
    timeslot_begin = models.TimeField(blank=True, null=True)
    timeslot_end = models.TimeField(blank=True, null=True)
    show_name = models.CharField(blank=True, null=True, max_length=100)
    broadcast_length = timedelta.TimedeltaField(blank=True, null=True, help_text="The easiest way to enter time is as <em>XX minutes, YY seconds</em> or <em>YY seconds</em>.")
    num_spots = models.IntegerField(blank=True, null=True, verbose_name="Number of Spots")
    rate = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text="Dollar cost for each spot")

