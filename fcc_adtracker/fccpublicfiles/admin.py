from django.contrib import admin
from django import forms
from .models import *
from .views import *

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

import reversion

import weekday_field

CALLSIGNS_LIST = map(lambda x: x[1], CALLSIGNS)

POLITICAL_SPOT_FIELDS = (('airing_start_date', 'airing_end_date', 'airing_days',), ('timeslot_begin', 'timeslot_end'), 'show_name', ('broadcast_length', 'num_spots', 'rate'))


class PoliticalSpotAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalSpot
    airing_days = weekday_field.forms.WeekdayFormField(required=False)


class PoliticalSpotAdmin(reversion.VersionAdmin):
    form = make_ajax_form(PoliticalSpot, {'show_name': ' show_name'}, superclass=PoliticalSpotAdminForm)
    search_fields = ['advertiser__name', 'bought_by__name']
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


class PoliticalBuyAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalBuy


class PoliticalBuyAdmin(reversion.VersionAdmin, AjaxSelectAdmin):
    # form = PoliticalBuyAdminForm
    form = make_ajax_form(PoliticalBuy, {
                          'advertiser': 'advertiser',
                          'advertiser_signatory': 'person',
                          'bought_by': 'media_buyer',
                          'station': 'callsign',
                          'documentcloud_doc': 'doccloud'
                          })
    save_on_top = True
    list_display = ('documentcloud_doc', 'station', 'advertiser', 'advertiser_signatory', 'bought_by')
    search_fields = ['advertiser__name', 'bought_by__name', 'station']
    inlines = [PoliticalSpotInline, ]

admin.site.register(PoliticalBuy, PoliticalBuyAdmin)


class RoleAdminInline(admin.StackedInline):
    model = Role
    extra = 1
    form = make_ajax_form(Role, {'organization': 'organization', 'person': 'person', 'title': 'role_title'})


class RoleAdmin(reversion.VersionAdmin, AjaxSelectAdmin):
    form = make_ajax_form(Role, {'organization': 'organization', 'person': 'person', 'title': 'role_title'})
    list_display = ('person', 'title', 'organization')
    search_fields = ['organization__name', ]
admin.site.register(Role, RoleAdmin)


class AddressAdmin(reversion.VersionAdmin, AjaxSelectAdmin):
    list_display = ('__unicode__', 'city', 'state')
    list_filter = ('state',)
admin.site.register(Address, AddressAdmin)


class OrganizationAdmin(reversion.VersionAdmin, AjaxSelectAdmin):
    list_display = ('name', 'fec_id', 'organization_type')
    search_fields = ['name', 'fec_id']
    form = make_ajax_form(Organization, {'addresses': 'address'})
    inlines = [RoleAdminInline, ]


class PersonAdmin(reversion.VersionAdmin, AjaxSelectAdmin):
    list_display = ('last_name', 'first_name', 'middle_name')
    search_fields = ['last_name', 'first_name']
    # form = make_ajax_form(Person,{'organization':'organization'})
    inlines = [RoleAdminInline, ]

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
