from django.contrib import admin
from django import forms
from .models import PoliticalSpot, PoliticalBuy, Role, Organization, Person

from reversion import VersionAdmin
from moderation.admin import ModerationAdmin
from moderation.forms import BaseModeratedObjectForm

import weekday_field

POLITICAL_SPOT_FIELDS = (('airing_start_date', 'airing_end_date', 'airing_days',), ('timeslot_begin', 'timeslot_end'), 'show_name', ('broadcast_length', 'num_spots', 'rate'))


class PoliticalSpotAdminForm(BaseModeratedObjectForm):
    class Meta:
        model = PoliticalSpot
    airing_days = weekday_field.forms.WeekdayFormField(required=False)


class PoliticalSpotAdmin(ModerationAdmin, VersionAdmin):
    form = PoliticalSpotAdminForm
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
    form = PoliticalSpotAdminForm
    fieldsets = (
        (None, {
            'fields': POLITICAL_SPOT_FIELDS
        }),
    )


class PoliticalBuyAdminForm(BaseModeratedObjectForm):
    class Meta:
        model = PoliticalBuy


class PoliticalBuyAdmin(ModerationAdmin, VersionAdmin):
    form = PoliticalBuyAdminForm
    save_on_top = True
    list_display = ('documentcloud_doc', 'advertiser', 'advertiser_signatory', 'bought_by')
    search_fields = ['advertiser__name', 'bought_by__name', 'broadcasters__callsign']
    inlines = [PoliticalSpotInline, ]

admin.site.register(PoliticalBuy, PoliticalBuyAdmin)


class RoleAdminInline(admin.StackedInline):
    model = Role
    extra = 1


class RoleAdmin(ModerationAdmin, VersionAdmin):
    list_display = ('person', 'title', 'organization')
    search_fields = ['organization__name', ]
admin.site.register(Role, RoleAdmin)


class OrganizationAdmin(ModerationAdmin, VersionAdmin):
    list_display = ('name', 'fec_id', 'organization_type')
    search_fields = ['name', 'fec_id']
    # inlines = [RoleAdminInline, ]


class PersonAdmin(ModerationAdmin, VersionAdmin):
    model = Person
    list_display = ('last_name', 'first_name', 'middle_name')
    search_fields = ['last_name', 'first_name']
    inlines = [RoleAdminInline, ]

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
