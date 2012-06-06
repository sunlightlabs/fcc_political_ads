from django.contrib import admin
from .models import *
from .views import *
from django.contrib.admin import widgets


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'state', 'is_a',)
    list_filter = ('is_a', 'state',)

admin.site.register(Profile, ProfileAdmin)
