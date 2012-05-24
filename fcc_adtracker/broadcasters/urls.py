from django.conf.urls import patterns, include, url

urlpatterns = patterns('broadcasters',
    url(r'^states/(?P<state_id>\w{2})/$', 'views.state_broadcaster_list', name='state_broadcaster_list'),
    # url(r'^states/$', 'views.state_broadcaster_list', name='broadcaster_state_list'),
    url(r'^nearby.json$', 'views.nearest_broadcasters_list', name='nearest_broadcasters_list'),
    url(r'^station/(?P<callsign>[\w-]+)/$', 'views.broadcaster_detail', name='broadcaster_detail'),
    # url(r'^edit/station/(?P<callsign>[\w-]+)/$', 'views.edit_broadcaster', name='edit_broadcaster'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
