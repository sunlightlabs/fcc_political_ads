from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

from doccloud.models import Document

import reversion

from locations.models import Address
from broadcasters.models import Broadcaster
import datetime
import timedelta
from weekday_field import fields as wf_fields


ORGANIZATION_TYPES = (
    (u'MB', u'MediaBuyer'),
    (u'AD', u'Advertiser'),
)

DOCUMENTCLOUD_META = getattr(settings, 'DOCUMENTCLOUD_META', {})


class Person(models.Model):
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40)
    suffix = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = "People"
        ordering = ('last_name', 'first_name',)

    def full_name():
        doc = "Full name of the person, as calculated"

        def fget(self):
            name_parts = [self.first_name, self.last_name]
            if self.middle_name:
                name_parts.insert(1, self.middle_name)
            if self.suffix:
                name_parts.append(self.suffix)
            return u' '.join(name_parts)
        return locals()
    full_name = property(**full_name())

    def __unicode__(self):
        return self.full_name


class Organization(models.Model):
    name = models.CharField(max_length=100)
    organization_type = models.CharField(blank=True, max_length=2, choices=ORGANIZATION_TYPES)
    addresses = models.ManyToManyField(Address, blank=True, null=True)
    employees = models.ManyToManyField(Person, through='Role')
    fec_id = models.CharField(max_length=9, blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        if self.name:
            return self.name
        return u"Organization"


class Role(models.Model):
    person = models.ForeignKey(Person)
    organization = models.ForeignKey(Organization)
    title = models.CharField(max_length=100, help_text="Job title or descriptor for position they hold.")

    def __unicode__(self):
        return u"<" + self.person.__unicode__() + ": " + self.title + " >"


class GenericPublicDocument(models.Model):
    documentcloud_doc = models.ForeignKey(Document)
    broadcasters = models.ManyToManyField(Broadcaster, null=True)


class PoliticalBuy(models.Model):
    """A subset of PublicFile, the PoliticalBuy records purchases of air time (generally for political ads)"""
    documentcloud_doc = models.ForeignKey(Document)
    contract_number = models.CharField(blank=True, max_length=100)
    advertiser = models.ForeignKey('Organization', blank=True, null=True, related_name='advertiser_politicalbuys', limit_choices_to={'organization_type': u'AD'})
    advertiser_signatory = models.ForeignKey('Person', blank=True, null=True)
    bought_by = models.ForeignKey('Organization', blank=True, null=True,
                                  related_name='mediabuyer_politicalbuys',
                                  limit_choices_to={'organization_type': u'MB'},
                                  help_text="The media buyer"
                                  )
    contract_start_date = models.DateField(blank=True, null=True, default=datetime.date.today)
    contract_end_date = models.DateField(blank=True, null=True, default=datetime.date.today)
    lowest_unit_price = models.NullBooleanField(default=None, blank=True, null=True)
    total_spent_raw = models.IntegerField(blank=True, null=True)

    broadcasters = models.ManyToManyField(Broadcaster, null=True)

    def __unicode__(self):
        if self.documentcloud_doc:
            return u"{0}: {1}".format(', '.join([x.callsign for x in self.broadcasters.all()[:5]]), self.documentcloud_doc)
        return u"PoliticalBuy"

    def total_spent(self):
        """ Returns a total spent figure, from either the grand total on the document, or calculated from ad buys. """
        # TODO: we may want to have this also return a calculation if available, if the raw total is not filled in
        return self.total_spent_raw


# Maybe update doccloud with fec_id if we have one?
# @receiver(post_save, sender=PoliticalBuy)
# def set_doccloud_data(sender, instance, signal, *args, **kwargs):
#     doccloud_data = copy.deepcopy(DOCUMENTCLOUD_META)
#     doccloud_data['callsign'] = instance.station

# @receiver(post_save, sender=PoliticalBuy)
# def set_doccloud_data(sender, instance, signal, *args, **kwargs):
#     doc = instance.documentcloud_doc
#     doccloud_data = copy.deepcopy(DOCUMENTCLOUD_META)
#     doccloud_data['callsign'] = instance.broadcasters.latest('id').callsign
#     if doc.dc_data != doccloud_data:
#         doc.dc_data = doccloud_data


@receiver(pre_delete, sender=PoliticalBuy)
def set_privacy_for_deassociated_docs(sender, instance, *args, **kwargs):
    # Caution when PoliticalBuy or Document(Cloud) models are deleted: Make DocumentCloud doc private, but don't delete.
    doc = instance.documentcloud_doc
    doc.access_level = 'private'
    doc.dc_properties.update_access(doc.access_level)
    doc.save()


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

    def __unicode__(self):
        name_string = u'PoliticalSpot'
        if self.document and self.document.advertiser:
            name_string = u'{0}'.format(self.document.advertiser)
            # if self.document.station:
                # name_string = u'{0} on {1}'.format(name_string, self.document.station)
        if self.show_name:
                name_string = u'{0}: "{1}"'.format(name_string, self.show_name)
        if self.airing_start_date:
            name_string = u'{0} ({1} to {2})'.format(name_string, self.airing_start_date, self.airing_end_date)
        return name_string


reversion.register(Person, follow=['role_set', 'organization_set', 'politicalbuy_set'])
reversion.register(Role, follow=['person', 'organization'])
reversion.register(Organization, follow=['employees', 'role_set'])
#reversion.register(Document)
reversion.register(PoliticalBuy)
reversion.register(PoliticalSpot)
