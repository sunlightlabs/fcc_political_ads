from django.contrib import admin
from django import forms
from .models import *
from django.contrib.admin import widgets
from bootstrapper.widgets import TypeaheadTextInput


CALLSIGNS_LIST = map(lambda x: x[1], CALLSIGNS)

# TODO make endpoint for on-the-fly generation ot the advertiser list, other lists
ADVERTISER_LIST = [p.advertiser for p in PoliticalBuy.objects.only('advertiser').exclude(advertiser='')]

class PoliticalSpotAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalSpot



class PoliticalSpotAdmin(admin.ModelAdmin):
    form = PoliticalSpotAdminForm
    fieldsets = (
        (None, {
            'fields': ('document',)
        }),
        (None, {
            'fields': (('airing_start_date', 'airing_end_date'), ('timeslot_begin', 'timeslot_end'), 'show_name', ('broadcast_length', 'num_spots', 'rate'))
        }),
    )

admin.site.register(PoliticalSpot, PoliticalSpotAdmin)


class PoliticalSpotInline(admin.StackedInline):
    model = PoliticalSpot
    fieldsets = (
        (None, {
            'fields': (('airing_start_date', 'airing_end_date'), ('timeslot_begin', 'timeslot_end'), 'show_name', ('broadcast_length', 'num_spots', 'rate'))
        }),
    )

class PoliticalBuyAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalBuy

    station = forms.CharField(widget=TypeaheadTextInput(data_source=list(CALLSIGNS_LIST)))
    advertiser = forms.CharField(required=False, widget=TypeaheadTextInput(data_source=list(ADVERTISER_LIST)))

class PoliticalBuyAdmin(admin.ModelAdmin):
    form = PoliticalBuyAdminForm
    save_on_top = True
    list_display = ('documentcloud_doc', 'station', 'advertiser', 'ordered_by')
    inlines = [
       PoliticalSpotInline,
    ]

admin.site.register(PoliticalBuy, PoliticalBuyAdmin)