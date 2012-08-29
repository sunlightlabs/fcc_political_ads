from ajax_select import LookupChannel
from django.utils.html import escape
from .models import *


class BroadcasterLookup(LookupChannel):

    model = Broadcaster
    min_length = 2

    def get_query(self, q, request):
        return Broadcaster.objects.filter(callsign__istartswith=q).order_by('callsign')

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
            """ (HTML) formatted item for displaying item in the selected deck area """
            return u"{callsign} ({network_affiliate} {channel})<div>State: {state}</div>".format(callsign=escape(obj.callsign), network_affiliate=escape(obj.network_affiliate or ''), channel=escape(obj.channel or ''), state=escape(obj.community_state))
