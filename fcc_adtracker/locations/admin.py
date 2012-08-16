from django.contrib import admin

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from reversion import VersionAdmin
from moderation.admin import ModerationAdmin
from moderation.forms import BaseModeratedObjectForm

from .models import Address, AddressLabel


class AddressAdmin(AjaxSelectAdmin, ModerationAdmin, VersionAdmin):
    list_display = ('__unicode__', 'city', 'state')
    list_filter = ('state',)
admin.site.register(Address, AddressAdmin)


