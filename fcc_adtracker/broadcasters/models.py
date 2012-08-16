from __future__ import division
from django.db import models
from django.contrib.localflavor.us import us_states
from django.contrib.localflavor.us.models import USStateField
import datetime


STATES_DICT = dict(us_states.US_STATES)


class Broadcaster(models.Model):
    """Broadcaster, based on FCC's CDBS facility table"""
    callsign = models.CharField(max_length=12, unique=True)
    channel = models.PositiveSmallIntegerField(null=True, blank=True)
    nielsen_dma = models.CharField(max_length=60, blank=True, null=True, help_text='Nielsen Designated Market Area')
    network_affiliate = models.CharField(max_length=100, blank=True, null=True)
    facility_id = models.PositiveIntegerField(blank=True, null=True, unique=True, editable=False, help_text='FCC assigned id')
    facility_type = models.CharField(max_length=3, blank=True, null=True, help_text='FCC assigned facility_type')
    community_city = models.CharField(max_length=20, blank=True, null=True)
    community_state = USStateField(choices=us_states.US_STATES, blank=True, null=True)
    addresses = models.ManyToManyField('Address', through='BroadcasterAddress', blank=True, null=True)

    class Meta:
        ordering = ('community_state', 'community_city', 'callsign')

    def fcc_profile_url():
        def fget(self):
            return u'https://stations.fcc.gov/station-profile/{0}'.format(self.callsign.lower())
        return locals()
    fcc_profile_url = property(**fcc_profile_url())

    @models.permalink
    def get_absolute_url(self):
        return ('fccpublicfiles.views.broadcaster_detail', (), {'callsign': self.callsign})

    def __unicode__(self):
        if self.callsign:
            disp_name = self.callsign
            disp_elements = ('community_state', 'network_affiliate', 'channel')
            extra_info = ', '.join([str(val) for val in [self.__getattribute__(el) for el in disp_elements] if val != None])
            return '{0} [{1}]'.format(disp_name, extra_info)
        return u"Broadcaster"



class BroadcasterAddress(models.Model):
    broadcaster = models.ForeignKey('Broadcaster')
    address = models.ForeignKey('Address')
    label = models.ForeignKey('AddressLabel')

    class Meta:
        verbose_name_plural = u'Broadcaster Addresses'
        unique_together = (('broadcaster', 'address', 'label'),)

    def __unicode__(self):
        return u"{0}'s '{1}' address".format(self.broadcaster.callsign, self.label)
