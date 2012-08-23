from django.conf.urls import patterns, include, url
from broadcasters.urls import json_urlpatterns
from ajax_select import urls as ajax_select_urls
from fccpublicfiles.views import prelim_doc_form

from django.contrib import admin
import moderation.helpers

moderation.helpers.auto_discover()
admin.autodiscover()


urlpatterns = patterns('',
    url(r'', include('volunteers.urls')),
    # url(r'^publicfiles/', include('fccpublicfiles.urls')),
    url(r'^stations/', include(json_urlpatterns)),
    url(r'^states/(?P<state_id>\w{2})/$', 'broadcasters.views.state_broadcaster_list', name='state_broadcaster_list'),
    url(r'^$', 'fcc_adtracker.views.home_view', name='home'),
    (r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/fccpublicfiles/', include('fccpublicfiles.admin_urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^document/submit/', 'fccpublicfiles.views.prelim_doc_form', name='document_submit'),
    url(r'^document/success/', 'fccpublicfiles.views.doc_success', name='document_success'),
)
