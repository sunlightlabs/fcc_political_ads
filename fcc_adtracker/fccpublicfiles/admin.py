from django.contrib import admin
from django import forms
from .models import *
from django.contrib.admin import widgets
from bootstrapper.widgets import TypeaheadTextInput


CALLSIGNS_LIST = map(lambda x: x[1], CALLSIGNS)

# TODO make endpoint for on-the-fly generation ot the advertiser list, other lists
ADVERTISER_LIST = [p.advertiser for p in PoliticalDocument.objects.only('advertiser').exclude(advertiser='')]

class PoliticalAdAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalAd



class PoliticalAdAdmin(admin.ModelAdmin):
    form = PoliticalAdAdminForm
    fieldsets = (
        (None, {
            'fields': ('document',)
        }),
        (None, {
            'fields': (('airing_start_date', 'airing_end_date'), ('timeslot_begin', 'timeslot_end'), 'show_name', ('broadcast_length', 'num_spots', 'rate'))
        }),
    )

admin.site.register(PoliticalAd, PoliticalAdAdmin)


class PoliticalAdInline(admin.StackedInline):
    model = PoliticalAd
    fieldsets = (
        (None, {
            'fields': (('airing_start_date', 'airing_end_date'), ('timeslot_begin', 'timeslot_end'), 'show_name', ('broadcast_length', 'num_spots', 'rate'))
        }),
    )
    
class PoliticalDocumentAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalDocument

    station = forms.CharField(widget=TypeaheadTextInput(data_source=list(CALLSIGNS_LIST)))
    advertiser = forms.CharField(required=False, widget=TypeaheadTextInput(data_source=list(ADVERTISER_LIST)))

class PoliticalDocumentAdmin(admin.ModelAdmin):
    form = PoliticalDocumentAdminForm
    save_on_top = True
    list_display = ('documentcloud_doc', 'station', 'advertiser', 'ordered_by')
    inlines = [
       PoliticalAdInline,
    ]

admin.site.register(PoliticalDocument, PoliticalDocumentAdmin)