from __future__ import division
from django.db import models
from django.contrib.localflavor.us import us_states
from django.contrib.localflavor.us.models import USStateField
import datetime

from locations.models import Address, AddressLabel


STATES_DICT = dict(us_states.US_STATES)


class Broadcaster(models.Model):
    """Broadcaster, based on FCC's CDBS facility table"""
    callsign = models.CharField(max_length=12, unique=True)
    channel = models.PositiveSmallIntegerField(null=True, blank=True)
    nielsen_dma = models.CharField(max_length=60, blank=True, null=True, help_text='Nielsen Designated Market Area')
    dma_id = models.PositiveIntegerField(blank=True, null=True, editable=False, help_text='DMA ID, from Nielsen')
    network_affiliate = models.CharField(max_length=100, blank=True, null=True)
    facility_id = models.PositiveIntegerField(blank=True, null=True, unique=True, editable=False, help_text='FCC assigned id')
    facility_type = models.CharField(max_length=3, blank=True, null=True, help_text='FCC assigned facility_type')
    community_city = models.CharField(max_length=20, blank=True, null=True)
    community_state = USStateField(choices=us_states.US_STATES, blank=True, null=True)
    

    class Meta:
        ordering = ('community_state', 'community_city', 'callsign')

    def fcc_profile_url():
        def fget(self):
            return u'https://stations.fcc.gov/station-profile/{0}'.format(self.callsign.lower())
        return locals()
    fcc_profile_url = property(**fcc_profile_url())

    @models.permalink
    def get_absolute_url(self):
        return ('broadcasters.views.broadcaster_detail', (), {'callsign': self.callsign})

    def __unicode__(self):
        if self.callsign:
            disp_elements = {
                'callsign': self.callsign,
                'community_state': self.community_state,
                'community_city': self.community_city,
                'network_affiliate': self.network_affiliate,
                'channel': self.channel
            }
            output_str = u'{callsign}'.format(**disp_elements)
            if disp_elements['network_affiliate'] and disp_elements['channel']:
                output_str = u'{0} ({network_affiliate} channel {channel}, {community_city}, {community_state})'.format(output_str, **disp_elements)
            return output_str
        return u"Broadcaster"


class BroadcasterAddress(models.Model):
    broadcaster = models.ForeignKey('Broadcaster')
    address = models.ForeignKey(Address)
    label = models.ForeignKey(AddressLabel)

    class Meta:
        verbose_name_plural = u'Broadcaster Addresses'
        unique_together = (('broadcaster', 'address', 'label'),)

    def __unicode__(self):
        return u"{0}'s '{1}' address".format(self.broadcaster.callsign, self.label)
