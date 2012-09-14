from django.contrib import admin
from ajax_select.admin import AjaxSelectAdmin
from reversion import VersionAdmin
from .models import Address


class AddressAdmin(AjaxSelectAdmin, VersionAdmin):
    list_display = ('__unicode__', 'city', 'state')
    list_filter = ('state',)
admin.site.register(Address, AddressAdmin)
