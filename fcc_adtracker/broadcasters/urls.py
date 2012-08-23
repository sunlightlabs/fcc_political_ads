from django.conf.urls import patterns, include, url


json_urlpatterns = patterns('broadcasters.json_views',
                            url(r'^nearby.json$', 'nearest_broadcasters_list', name='nearest_broadcasters_list'),
                            url(r'^by-state/(?P<state_id>\w{2})/all.json$', 'state_broadcasters_json', name='state_broadcasters_json'),
                            url(r'^by-state/(?P<state_id>\w{2})/addresses/(?P<label_slug>[\w-]+).json$', 'state_broadcaster_addresses', name='state_broadcaster_addresses'),)

urlpatterns = patterns('broadcasters.views',
                       url(r'^by-state/(?P<state_id>\w{2})/$', 'state_broadcaster_list', name='state_broadcaster_list'),
                       url(r'^by-state/$', 'state_broadcaster_list', name='broadcaster_state_list'),
                       url(r'^(?P<callsign>[\w-]+)/$', 'views.broadcaster_detail', name='broadcaster_detail'),
                       url(r'^json/', include(json_urlpatterns)))
