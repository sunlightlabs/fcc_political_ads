from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from broadcasters.urls import json_urlpatterns
from ajax_select import urls as ajax_select_urls

from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^account/$', 'fcc_adtracker.views.user_dashboard', name='user_dashboard'),
    url(r'^about/', direct_to_template, {'template': 'about.html'}),
    url(r'^help/', direct_to_template, {'template': 'help.html'}),
    url(r'', include('volunteers.urls')),
    url(r'', include('sfapp.urls')),
    url(r'', include('fccpublicfiles.urls')),
    url(r'^fcc/', include('scraper.urls')),
    (r'^search/', include('search.urls')),

    url(r'^stations/json/', include(json_urlpatterns)),
    #url(r'^stations/', include('broadcasters.urls')),
#    url(r'^states/(?P<state_id>\w{2})/$', 'broadcasters.views.state_broadcaster_list', name='state_broadcaster_list'),
#    url(r'^states/$', 'broadcasters.views.state_list', name='state_list'),
    url(r'^$', 'fcc_adtracker.views.home_view', name='home'),

    (r'^admin/lookups/', include(ajax_select_urls)),
    (r'^admin/', include('stronger_auth.auth_urls')),
    url(r'^admin/', include(admin.site.urls)),
)
