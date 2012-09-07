from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from volunteers.models import Profile, NonUserProfile
from volunteers.forms import NonUserProfileForm


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state', 'is_a',)
    list_filter = ('is_a', 'state',)

admin.site.register(Profile, ProfileAdmin)


class NonUserProfileAdmin(admin.ModelAdmin):
    model = NonUserProfile
    form = NonUserProfileForm
    date_hierarchy = 'date_created'
    list_display = ('email', 'last_name', 'first_name', 'phone', 'city', 'state', 'zipcode', 'is_a')
    list_filter = ('is_a', 'state',)
    fieldsets = (
        ('Basics', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Location', {
            'fields': ('city', 'state', 'zipcode')
        }),
        ('Sharing', {
            'fields': ('share_info',)
        })
    )

    def queryset(self, request):
        qs = super(NonUserProfileAdmin, self).queryset(request)
        if not request.user.has_perm('volunteers.view_unshared_profile') and not request.user.is_superuser:
            qs = qs.filter(share_info=True)
        return qs


admin.site.register(NonUserProfile, NonUserProfileAdmin)

# Not sure where the right place to put admin overrides is, so just putting this here. 
class UserAdmin(UserAdmin):
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

