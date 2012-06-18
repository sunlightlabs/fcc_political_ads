from django.contrib import admin
from django import forms
from .models import *
from .views import *
from django.contrib.admin import widgets

# from bootstrapper.widgets import TypeaheadTextInput
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
# import autocomplete_light

import reversion

import weekday_field

CALLSIGNS_LIST = map(lambda x: x[1], CALLSIGNS)

POLITICAL_SPOT_FIELDS = (('airing_start_date', 'airing_end_date', 'airing_days',), ('timeslot_begin', 'timeslot_end'), 'show_name', ('broadcast_length', 'num_spots', 'rate'))

class PoliticalSpotAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalSpot
    airing_days = weekday_field.forms.WeekdayFormField()


class PoliticalSpotAdmin(reversion.VersionAdmin):
    form = PoliticalSpotAdminForm
    
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
    form = PoliticalSpotAdminForm
    fieldsets = (
        (None, {
            'fields': POLITICAL_SPOT_FIELDS
        }),
    )

class PoliticalBuyAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalBuy

    # station = forms.CharField(widget=TypeaheadTextInput())
    # advertiser = forms.CharField(required=False, widget=TypeaheadTextInput())
    # advertiser_signatory = forms.CharField(required=False, widget=TypeaheadTextInput())

class PoliticalBuyAdmin(reversion.VersionAdmin, AjaxSelectAdmin):
    # form = PoliticalBuyAdminForm
    form = make_ajax_form(PoliticalBuy,{'advertiser':'organization', 'advertiser_signatory': 'person', 'bought_by':'organization'})
    # form = autocomplete_light.modelform_factory(PoliticalBuy)
    save_on_top = True
    list_display = ('documentcloud_doc', 'station', 'advertiser', 'advertiser_signatory', 'bought_by')
    inlines = [
       PoliticalSpotInline,
    ]

admin.site.register(PoliticalBuy, PoliticalBuyAdmin)

class RoleAdminInline(admin.StackedInline):
    model = Role
    extra = 1


class RoleAdmin(reversion.VersionAdmin):
    list_display = ('person', 'title', 'organization')
admin.site.register(Role, RoleAdmin)


class AddressAdmin(reversion.VersionAdmin):
    list_display = ('__unicode__', 'city', 'state')
    list_filter = ('state',)
admin.site.register(Address, AddressAdmin)


class OrganizationAdmin(reversion.VersionAdmin):
    list_display = ('name', 'fec_id', 'organization_type')
    inlines = [
       RoleAdminInline,
    ]

class PersonAdmin(reversion.VersionAdmin):
    list_display = ('last_name', 'first_name', 'middle_name')
    inlines = [
       RoleAdminInline,
    ]

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)