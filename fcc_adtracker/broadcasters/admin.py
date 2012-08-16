from django.contrib import admin
from django import forms
from .models import Broadcaster, BroadcasterAddress

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
