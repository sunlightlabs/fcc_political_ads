from django.contrib import admin
from django import forms
from .models import *
from django.contrib.admin import widgets


class PoliticalAdAdminForm(forms.ModelForm):
    class Meta:
        model = PoliticalAd

    broadcast_length = forms.TimeField( required=False, 
                                        input_formats=('%S','%M:%S','%H:%M:%S'),
                                        help_text="Allowed formats: <em>Seconds</em>, <em>MM:SS</em>, <em>HH:MM:SS</em>",
                                        widget=widgets.AdminTimeWidget())



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

    # station = forms.ChoiceField(widget=forms.Select(attrs={'class':'typeahead'}), choices=PublicDocument.station.choices)


class PoliticalDocumentAdmin(admin.ModelAdmin):
    form = PoliticalDocumentAdminForm
    list_display = ('documentcloud_doc', 'station', 'advertiser', 'ordered_by')
    inlines = [
       PoliticalAdInline,
    ]

admin.site.register(PoliticalDocument, PoliticalDocumentAdmin)