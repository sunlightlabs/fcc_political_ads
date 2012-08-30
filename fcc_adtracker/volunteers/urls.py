from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^signup/$', 'volunteers.views.noaccount_signup', name='noaccount_signup'),
    url(r'^account/register/$', 'volunteers.views.register_volunteer', name='register_volunteer'),
    url(r'^account/setup-profile/$', 'volunteers.views.setup_profile', name='setup_profile'),
    url(r'^account/profile/edit/$', 'volunteers.views.edit_profile', name='edit_profile'),
    url(r'^account/profile/$', 'volunteers.views.view_profile', name='view_profile'),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^account/error/$', 'volunteers.views.account_error', name='account_error'),
    url(r'^account/', include('registration.backends.default.urls')),
    url(r'^account/', include('social_auth.urls')),
    url(r'^account/$', 'volunteers.views.account_landing', name='account_landing'),
)
