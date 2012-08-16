from django.conf.urls import patterns, include, url


urlpatterns = patterns('broadcasters',
    url(r'^states/(?P<state_id>\w{2})/$', 'views.state_broadcaster_list', name='state_broadcaster_list'),
    # url(r'^states/$', 'views.state_broadcaster_list', name='broadcaster_state_list'),
    url(r'^stations/nearby.json$', 'views.nearest_broadcasters_list', name='nearest_broadcasters_list'),
    url(r'^stations/(?P<callsign>[\w-]+)/$', 'views.broadcaster_detail', name='broadcaster_detail'),
    url(r'^stations/(?P<state_id>\w{2})/addresses/(?P<label_slug>[\w-]+).json$', 'views.state_broadcaster_addresses', name='state_broadcaster_addresses'),
)
