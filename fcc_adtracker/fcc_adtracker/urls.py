from django.conf.urls import patterns, include, url
from broadcasters.urls import json_urlpatterns
from ajax_select import urls as ajax_select_urls
from fccpublicfiles.views import prelim_doc_form

from django.contrib import admin
import moderation.helpers

moderation.helpers.auto_discover()
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^account/dashboard/$', 'fcc_adtracker.views.user_dashboard', name='user_dashboard'),
    url(r'^account/$', 'fcc_adtracker.views.account_to_dashboard_landing', name='account_to_dashboard'),
    url(r'', include('volunteers.urls')),
    url(r'', include('sfapp.urls')),
    url(r'', include('fccpublicfiles.urls')),

    url(r'^stations/json/', include(json_urlpatterns)),
    # url(r'stations', include('broadcasters.urls')),
    url(r'^states/(?P<state_id>\w{2})/$', 'broadcasters.views.state_broadcaster_list', name='state_broadcaster_list'),
    url(r'^$', 'fcc_adtracker.views.home_view', name='home'),
    (r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
