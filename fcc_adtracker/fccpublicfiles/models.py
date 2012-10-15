from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.db.models import Sum
from django.dispatch import receiver
from django.conf import settings
from django.template.defaultfilters import slugify
from django_extensions.db.fields import UUIDField
from doccloud.models import Document
from scraper.models import PDF_File
from broadcasters.models import Broadcaster
from locations.models import Address
from fecdata.models import Candidate, Committee
from mildmoderator.managers import MildModeratedModelManager
from mildmoderator.models import MildModeratedModel
from weekday_field import fields as wf_fields
from uuid import uuid4
from django.contrib.localflavor.us import us_states


from fccpublicfiles.managers import PoliticalDocStatusManager

STATES_DICT = dict(us_states.US_STATES)

import copy
import datetime
import timedelta
import reversion


ORGANIZATION_TYPES = (
    (u'MB', u'MediaBuyer'),
    (u'AD', u'Advertiser'),
)

DOCUMENTCLOUD_META = getattr(settings, 'DOCUMENTCLOUD_META', {})


class TV_Advertiser(models.Model):
    # The same person can run for two seats; if that's the case, prefer senate over house--typically they're in a safe seat in the house and are fighting over the senate seat. Not perfect, but it's basically impossible to sort out, especially since the people filing the forms are often wrong
    candidate =  models.ForeignKey(Candidate, null=True)
    candidate_name = models.CharField(max_length=255, blank=True, null=True)
    # Many advertisers are related to multiple C-records; one for the superpac, one for electioneering, one for non-committee, etc. Which one is the primary one? Generally prefer the hierarchy used by ad hawk.
    primary_committee = models.ForeignKey(Committee, related_name='primary committee', null=True)
    secondary_committees = models.ManyToManyField(Committee, null=True, related_name='secondary committees', help_text=" ")
    committee_name = models.CharField(max_length=255, blank=True, null=True)
    advertiser_name = models.CharField(max_length=255, blank=True, null=True, help_text="Usually most prominent committee name, if there is one. Starting place is ad hawk's mapping. Human editing required for Crossroads. ")

    # Hmm, not sure one is really needed
    ad_hawk_url = models.CharField(max_length=255, blank=True, null=True)
    ie_url = models.CharField(max_length=255, blank=True, null=True)
    ftum_url = models.CharField(max_length=255, blank=True, null=True)

    # Ad hawk doesn't cover candidate ads
    is_in_adhawk = models.NullBooleanField(null=True, help_text = "Was this in ad hawk?")

    # how many states have we played in
    num_states = models.PositiveIntegerField(blank=True, null=True)
    # how many states this week?
    num_recent_state = models.PositiveIntegerField(blank=True, null=True)
    ## ditto for dmas
    num_dmas = models.PositiveIntegerField(blank=True, null=True)
    num_recent_dmas = models.PositiveIntegerField(blank=True, null=True)

    num_broadcasters = models.PositiveIntegerField(blank=True, null=True)
    num_recent_broadcasters = models.PositiveIntegerField(blank=True, null=True)

    num_buys = models.PositiveIntegerField(blank=True, null=True)
    num_recent_buys = models.PositiveIntegerField(blank=True, null=True)

    total_amount_guess_high = models.PositiveIntegerField(blank=True, null=True)
    total_amount_guess = models.PositiveIntegerField(blank=True, null=True)
    total_amount_guess_low = models.PositiveIntegerField(blank=True, null=True)

    recent_amount_guess_high= models.PositiveIntegerField(blank=True, null=True)
    recent_amount_guess = models.PositiveIntegerField(blank=True, null=True)
    recent_amount_guess_low = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        if (self.candidate):
            return "%s (%s)" % (self.advertiser_name, self.candidate_name)
        else:
            return self.advertiser_name



# helper table for lookups
class TV_Advertiser_Alias(models.Model):
    parent =  models.ForeignKey(TV_Advertiser, null=True)
    advertiser_name_raw = models.CharField(max_length=255, blank=True, null=True)
    advertiser_name_clean = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.advertiser_name_raw
# TK: Station_Race, Acti


class Person(MildModeratedModel):
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


class Organization(MildModeratedModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    organization_type = models.CharField(blank=True, max_length=2, choices=ORGANIZATION_TYPES)
    addresses = models.ManyToManyField(Address, blank=True, null=True)
    employees = models.ManyToManyField(Person, through='Role')
    fec_id = models.CharField(max_length=9, blank=True, help_text="fec id of primary committee")
    related_advertiser = models.ForeignKey(TV_Advertiser, null=True)


    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        if self.name:
            return self.name
        return u"Organization"


class Role(MildModeratedModel):
    person = models.ForeignKey(Person)
    organization = models.ForeignKey(Organization)
    title = models.CharField(blank=True, null=True, max_length=100, help_text="Job title or descriptor for position they hold.")

    def __unicode__(self):
        return u"<" + self.person.__unicode__() + ": " + self.title + " >"


class GenericPublicDocument(MildModeratedModel):
    documentcloud_doc = models.ForeignKey(Document)
    broadcasters = models.ManyToManyField(Broadcaster, null=True)

    # TODO: this should either be dropped or updated to is_public like the rest,
    # but we didn't have this under moderation so it seems like this field's
    # existence might have been a mistake anyway
    is_visible = models.BooleanField(default=False)


class PoliticalBuy(MildModeratedModel):
    """A subset of PublicFile, the PoliticalBuy records purchases of air time (generally for political ads)"""
    # Don't require documents -- allows us to reference other documents w/out copying them to our account.
    documentcloud_doc = models.ForeignKey(Document, null=True, default=None)
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
    total_spent_raw = models.DecimalField(max_digits=19, decimal_places=2, null=True, verbose_name='Grand Total')
    num_spots_raw = models.PositiveIntegerField(null=True, verbose_name='Number of Ad Spots')

    # JF Adds
    # Are the summary fields completed? We're still using is_complete for this, actually.
    is_summarized = models.NullBooleanField(default=False, verbose_name="Data Entry Is Complete", help_text="Are all the summary fields filled in?")
    # Did this come from the FCC?
    is_FCC_doc = models.NullBooleanField(default=False, help_text="Did this document come from the FCC? ")
    related_FCC_file = models.ForeignKey(PDF_File, blank=True, null=True)
    is_invalid = models.NullBooleanField(default=False, help_text="Is this document unprocessable, a duplicate, or devoid of any relevant information? ", null=True)
    is_invoice = models.NullBooleanField(default=False, help_text="Is this document an invoice?xf", null=True)
    data_entry_notes = models.TextField(blank=True, null=True, help_text="Explain any complications in entering summary data")
    """ Fields migrated from PDF_File, but now here as well. """
    candidate_type = models.CharField(max_length=31, blank=True, null=True, help_text="candidate type in pdf_file")
    fcc_folder_name = models.CharField(max_length=255, blank=True, null=True, help_text="As raw name guess in pdf_file")
    nielsen_dma = models.CharField(max_length=60, blank=True, null=True, help_text='Nielsen Designated Market Area')
    dma_id =  models.PositiveIntegerField(blank=True, null=True, editable=False, help_text='DMA ID, from Nielsen')
    community_state = models.CharField(max_length=7, blank=True, null=True)
    ignore_post_save = models.NullBooleanField(default=False, null=True, help_text="flag to avoid calling doc_cloud needlessly")
    upload_time = models.DateField(blank=True, null=True, default=None)
    broadcaster_callsign = models.CharField(max_length=7, blank=True, null=True, help_text="first broadcaster callsign.")
    advertiser_display_name = models.CharField(max_length=211, blank=True, null=True)

    """ This is a user-defined setting that lets an authenticated user
    mark a record as not needing any more work. The idea is that
    a superuser will need to come along afterward to the moderated object
    and approve the "completeness".
    """

    is_complete = models.BooleanField(default=False, verbose_name="Data Entry Is Complete", )
    uuid_key = UUIDField(version=4, default=lambda: uuid4(), unique=True, editable=False)
    broadcasters = models.ManyToManyField(Broadcaster, null=True)

    def broadcasters_callsign_list(self):
        return [x.callsign for x in self.broadcasters.all()]

    def doc_source(self):
        if self.is_FCC_doc:
            return 'FCC'
        else:
            return 'Submission'

    def broadcasters_state_list(self):
        return [x.community_state for x in self.broadcasters.all()]

    def __unicode__(self):
        if self.documentcloud_doc:
            broadcasters_str = u', '.join(self.broadcasters_callsign_list()[:5])
            date_str = '-'.join([self.contract_start_date.__str__(), self.contract_end_date.__str__()])
            return u"{0} {1}: {2}".format(broadcasters_str, self.advertiser or '', date_str)
        return u"PoliticalBuy"

    def isadbuy(self):
        return True

    def advertiser_display(self):
        return self.advertiser or 'Unknown'

    def date_display(self):
        date_str = ''
        if self.is_FCC_doc:
            date_str = u"{0}".format(self.upload_time.strftime("%m/%d/%y"))
        else:
            date_str = u"{0}".format(self.contract_end_date.strftime("%m/%d/%y"))
        return date_str

    def citystate_display(self):
        try:
            first_broadcaster = self.broadcasters.all()[0]
            broadcaster = "%s, %s" % (first_broadcaster.community_city, first_broadcaster.community_state)
            return broadcaster
        except:
            return None

    def station_display(self):
        try:
            first_broadcaster = self.broadcasters.all()[0]
            return first_broadcaster.callsign
        except IndexError:
            return None

    def name(self):
        all_broadcasters = self.broadcasters.all()
        broadcaster = "Unknown"
        if len(all_broadcasters) > 0:
            first_broadcaster = self.broadcasters.all()[0]
            broadcaster = "%s (%s, %s)" % (first_broadcaster.callsign, first_broadcaster.community_city, first_broadcaster.community_state)
        advertiser = 'Unknown'
        if self.advertiser:
            advertiser = self.advertiser
        elif self.is_FCC_doc:
            advertiser = self.related_FCC_file.folder_name()
        date_str = ""
        if (self.contract_end_date):
            date_str = self.contract_end_date.strftime(", %m/%d/%y")

        return "%s%s on %s" % (advertiser, date_str, broadcaster)

    def nonunique_slug(self):
        return slugify(self.__unicode__())

    @models.permalink
    def get_absolute_url(self):
        return ('politicalbuy_view', (), {'uuid_key': str(self.uuid_key)})

    @models.permalink
    def get_edit_url(self):
        return ('politicalbuy_edit', (), {'uuid_key': str(self.uuid_key)})

    def get_station_url(self):
        return "/political-files/tv-station/%s/" % (self.broadcaster_callsign)

    def get_state_url(self):
        return "/political-files/state/%s/" % (self.community_state)

    def get_dma_url(self):
        return "/political-files/dma/%s/" % (self.dma_id)

    def total_spent(self):
        """ Returns a total spent figure, from either the grand total on the document, or calculated from ad buys. """
        # TODO: we may want to have this also return a calculation if available, if the raw total is not filled in
        return self.total_spent_raw

    def total_num_spots(self):
        """ Returns the sum of the num_spots values for all related political spot objects. """
        values = self.politicalspot_set.all().aggregate(total_num_spots=Sum('num_spots'))
        return values['total_num_spots']

    status_objects = PoliticalDocStatusManager()

    def doc_status(self):
        if self.is_invoice or self.is_invalid:
            return 'Summarized'
        elif self.total_spent_raw:
            if self.total_spent_raw > 0:
                return 'Summarized'
        elif self.is_FCC_doc and not self.related_FCC_file.in_document_cloud:
            return 'Not loaded'
        else:
            return 'Needs entry'

@receiver(post_save, sender=PoliticalBuy)
def set_doccloud_data(sender, instance, signal, *args, **kwargs):
    if instance.documentcloud_doc and not instance.ignore_post_save:
        doc = instance.documentcloud_doc
        #doccloud_data = copy.deepcopy(DOCUMENTCLOUD_META)
        doccloud_data = {}
        doccloud_data['callsign'] = [ str(x) for x in instance.broadcasters_callsign_list() ]

        if (instance.is_FCC_doc):
            doccloud_data['uploader'] = "auto"
            doccloud_data['Collection'] = 'PoliticalAdSleuthFCC'

        else:
            doccloud_data['uploader'] = "submission"
            # only put the manual documents here...
            doccloud_data['contributedto'] = "freethefiles"
            doccloud_data['Collection'] = 'PoliticalAdSleuth'

        if doc.dc_data != doccloud_data:
            doc.dc_data = doccloud_data




@receiver(pre_delete, sender=PoliticalBuy)
def set_privacy_for_deassociated_docs(sender, instance, *args, **kwargs):
    if instance.documentcloud_doc:
        # Caution when PoliticalBuy or Document(Cloud) models are deleted: Make DocumentCloud doc private, but don't delete.
        doc = instance.documentcloud_doc
        doccloud_data = copy.deepcopy(DOCUMENTCLOUD_META)
        doccloud_data['spasstatus'] = 'deleted'

        if doc.dc_data != doccloud_data:
            doc.dc_data = doccloud_data

        doc.access_level = 'private'
        doc.dc_properties.update_access(doc.access_level)
        doc.save()


class PoliticalSpot(MildModeratedModel):
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

# summary fields, previously only for FCC data.

class state_summary(models.Model):
    state_id = models.CharField(max_length=2, blank=True, null=True)
    num_broadcasters = models.PositiveIntegerField(blank=True, null=True, help_text="All broadcasters")
    num_mandated_broadcasters = models.PositiveIntegerField(blank=True, null=True, help_text="only mandated broadcasters")
    tot_buys = models.PositiveIntegerField(blank=True, null=True)
    pres_buys =  models.PositiveIntegerField(blank=True, null=True)
    sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    house_buys =  models.PositiveIntegerField(blank=True, null=True)
    state_buys = models.PositiveIntegerField(blank=True, null=True)
    local_buys = models.PositiveIntegerField(blank=True, null=True)
    outside_buys = models.PositiveIntegerField(blank=True, null=True)
    recent_pres_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_house_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_outside_buys = models.PositiveIntegerField(blank=True, null=True)
    total_files_entered = models.PositiveIntegerField(blank=True, null=True)
    tot_spending_from_entry = models.PositiveIntegerField(blank=True, null=True)
    tot_est_low = models.PositiveIntegerField(blank=True, null=True)
    tot_est_ave = models.PositiveIntegerField(blank=True, null=True)
    tot_est_high = models.PositiveIntegerField(blank=True, null=True)
    percent_estimated = models.PositiveIntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return "/political-files/state/%s/" % (self.state_id)

    def get_station_url(self):
        return "/political-files/stations/state/%s/" % (self.state_id)

    def name(self):
        return STATES_DICT.get(self.state_id, self.state_id)


class dma_summary(models.Model):
    dma_id = models.PositiveIntegerField(blank=True, null=True, editable=False, help_text='DMA ID, from Nielsen')
    dma_name = models.CharField(max_length=255, blank=True, null=True, help_text="Better name - set from file")
    fcc_dma_name = models.CharField(max_length=255, blank=True, null=True)
    rank1011 = models.PositiveIntegerField(blank=True, null=True)
    rank1112 = models.PositiveIntegerField(blank=True, null=True)

    num_broadcasters = models.PositiveIntegerField(blank=True, null=True, help_text="all broadcasters")
    num_mandated_broadcasters = models.PositiveIntegerField(blank=True, null=True, help_text="only mandated broadcasters")
    tot_buys = models.PositiveIntegerField(blank=True, null=True)
    pres_buys =  models.PositiveIntegerField(blank=True, null=True)
    sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    house_buys =  models.PositiveIntegerField(blank=True, null=True)
    state_buys = models.PositiveIntegerField(blank=True, null=True)
    local_buys = models.PositiveIntegerField(blank=True, null=True)
    outside_buys = models.PositiveIntegerField(blank=True, null=True)
    recent_pres_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_house_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_outside_buys = models.PositiveIntegerField(blank=True, null=True)
    total_files_entered = models.PositiveIntegerField(blank=True, null=True)
    tot_spending_from_entry = models.PositiveIntegerField(blank=True, null=True)
    tot_est_low = models.PositiveIntegerField(blank=True, null=True)
    tot_est_ave = models.PositiveIntegerField(blank=True, null=True)
    tot_est_high = models.PositiveIntegerField(blank=True, null=True)
    percent_estimated = models.PositiveIntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return "/political-files/dma/%s/" % (self.dma_id)

    def get_station_url(self):
        return "/political-files/stations/dma/%s/" % (self.dma_id)

    def name(self):
        return self.dma_name


reversion.register(Person, follow=['role_set', 'organization_set', 'politicalbuy_set'])
reversion.register(Role, follow=['person', 'organization'])
reversion.register(Organization, follow=['employees', 'role_set'])
#reversion.register(Document)
reversion.register(PoliticalBuy)
reversion.register(PoliticalSpot)
