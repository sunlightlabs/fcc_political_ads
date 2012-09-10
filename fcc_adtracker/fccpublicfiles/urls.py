from django.conf.urls import patterns, include, url

from django.contrib import admin
import moderation.helpers

from broadcasters import views as broadcaster_views

moderation.helpers.auto_discover()
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^political-files/submit/', 'fccpublicfiles.views.prelim_doc_form', name='document_submit'),
    url(r'^political-files/edit/(?P<buy_id>\d+)/', 'fccpublicfiles.views.politicalbuy_edit', name='politicalbuy_edit'),
    url(r'^political-files/add/advertiser/', 'fccpublicfiles.views.add_advertiser', name='add_advertiser'),
    url(r'^political-files/add/media-buyer/', 'fccpublicfiles.views.add_media_buyer', name='add_media_buyer'),
    url(r'^political-files/(?P<slug>\w|\-)+/(?P<buy_id>\d+)/$', 'fccpublicfiles.views.politicalbuy_view', name='politicalbuy_view'),
    url(r'^political-files/broadcaster/(?P<callsign>[\w-]+)/$', broadcaster_views.broadcaster_detail,
        {'template_name': 'broadcaster_politicalbuys.html'}, name='broadcaster_politicalbuys_view'),
)
