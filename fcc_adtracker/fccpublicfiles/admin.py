from django.contrib import admin
from django import forms
from .models import PoliticalSpot, PoliticalBuy, Role, Address, AddressLabel, Organization, \
        Person, Broadcaster, BroadcasterAddress

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

from reversion import VersionAdmin
from moderation.admin import ModerationAdmin
from moderation.forms import BaseModeratedObjectForm

import weekday_field


POLITICAL_SPOT_FIELDS = (('airing_start_date', 'airing_end_date', 'airing_days',), ('timeslot_begin', 'timeslot_end'), 'show_name', ('broadcast_length', 'num_spots', 'rate'))


class BroadcasterAddressInlineAdmin(admin.StackedInline):
    model = BroadcasterAddress
    extra = 1


class BroadcasterAddressAdmin(admin.ModelAdmin):
    model = BroadcasterAddress
    list_display = ('__unicode__', 'address', 'label')
    list_filter = ('label',)
    search_fields = ('broadcaster__callsign', 'label__name')

admin.site.register(BroadcasterAddress, BroadcasterAddressAdmin)


class BroadcasterAdmin(admin.ModelAdmin):
    model = Broadcaster
    list_display = ('callsign', 'channel', 'network_affiliate', 'community_city', 'community_state', 'display_fcc_profile_url')
    list_filter = ('community_state',)
    search_fields = ('callsign', 'community_city', 'community_state')
    filter_vertical = ('addresses',)
    readonly_fields = ('facility_id', 'facility_type')
    inlines = [BroadcasterAddressInlineAdmin,]
    fieldsets = (
        (None, {'fields': ('callsign', 'channel', 'network_affiliate')}),
        ('FCC DB fields', {
            'classes': ['collapse',],
            'fields': ('facility_id', 'facility_type')
        }),
        (None, {
            'fields': ('community_city', 'community_state')
        }),
        # (None, {
        #     'classes': ['wide',],
        #     'fields': {'addresses'}
        # })

    )

    def display_fcc_profile_url(self, obj):
        return u"<a target='_blank' href='{0}'>{1} FCC profile page</a>".format(obj.fcc_profile_url, obj.callsign)
    display_fcc_profile_url.short_description = u'FCC Profile Page'
    display_fcc_profile_url.allow_tags = True

admin.site.register(Broadcaster, BroadcasterAdmin)

class PoliticalSpotAdminForm(BaseModeratedObjectForm):
    class Meta:
        model = PoliticalSpot
    airing_days = weekday_field.forms.WeekdayFormField(required=False)


class PoliticalSpotAdmin(ModerationAdmin, VersionAdmin):
    form = make_ajax_form(PoliticalSpot, {'show_name': 'show_name'}, superclass=PoliticalSpotAdminForm)
    search_fields = ['advertiser__name', 'bought_by__name']
    list_display = ('__unicode__', 'show_name', 'airing_start_date', 'airing_end_date')
    list_filter = ('show_name',)
    fieldsets = (

        (None, {
            'fields': ('document',)
        }),
        (None, {
            'fields': POLITICAL_SPOT_FIELDS
        }),
    )

admin.site.register(PoliticalSpot, PoliticalSpotAdmin)


class PoliticalSpotInline(admin.StackedInline):
    model = PoliticalSpot
    form = make_ajax_form(PoliticalSpot, {'show_name': 'show_name'}, superclass=PoliticalSpotAdminForm)
    fieldsets = (
        (None, {
            'fields': POLITICAL_SPOT_FIELDS
        }),
    )


class PoliticalBuyAdminForm(BaseModeratedObjectForm):
    class Meta:
        model = PoliticalBuy


class PoliticalBuyAdmin(ModerationAdmin, VersionAdmin):
    # form = PoliticalBuyAdminForm
    form = make_ajax_form(PoliticalBuy, {
                          'advertiser': 'advertiser',
                          'advertiser_signatory': 'person',
                          'bought_by': 'media_buyer',
                          # 'station': 'callsign',
                          'documentcloud_doc': 'doccloud'
                          })
    save_on_top = True
    list_display = ('documentcloud_doc', 'advertiser', 'advertiser_signatory', 'bought_by')
    filter_horizontal = ('broadcasters',)
    search_fields = ['advertiser__name', 'bought_by__name', 'broadcasters__callsign']
    inlines = [PoliticalSpotInline, ]

admin.site.register(PoliticalBuy, PoliticalBuyAdmin)


class RoleAdminInline(admin.StackedInline):
    model = Role
    extra = 1
    form = make_ajax_form(Role, {'organization': 'organization', 'person': 'person', 'title': 'role_title'})


class RoleAdmin(AjaxSelectAdmin, ModerationAdmin, VersionAdmin):
    form = make_ajax_form(Role, {'organization': 'organization', 'person': 'person', 'title': 'role_title'})
    list_display = ('person', 'title', 'organization')
    search_fields = ['organization__name', ]
admin.site.register(Role, RoleAdmin)


class AddressLabelAdmin(admin.ModelAdmin):
    model = AddressLabel
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(AddressLabel, AddressLabelAdmin)


class AddressAdmin(AjaxSelectAdmin, ModerationAdmin, VersionAdmin):
    list_display = ('__unicode__', 'city', 'state', 'lat', 'lng')
    list_filter = ('state',)
admin.site.register(Address, AddressAdmin)


class OrganizationAdmin(AjaxSelectAdmin, ModerationAdmin, VersionAdmin):
    list_display = ('name', 'fec_id', 'organization_type')
    search_fields = ['name', 'fec_id']
    form = make_ajax_form(Organization, {'addresses': 'address'})
    inlines = [RoleAdminInline, ]


class PersonAdmin(AjaxSelectAdmin, ModerationAdmin, VersionAdmin):
    list_display = ('last_name', 'first_name', 'middle_name')
    search_fields = ['last_name', 'first_name']
    # form = make_ajax_form(Person,{'organization':'organization'})
    inlines = [RoleAdminInline, ]

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
