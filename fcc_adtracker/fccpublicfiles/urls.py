from django.conf.urls import patterns, include, url

from django.contrib import admin

from broadcasters import views as broadcaster_views

admin.autodiscover()

uuid_re_str = r'(?P<uuid_key>[a-f0-9-]{32,36})'

urlpatterns = patterns('',
    url(r'^political-files/submit/$', 'fccpublicfiles.views.prelim_doc_form', name='document_submit'),
    url(r'^political-files/needs-entry/', 'fccpublicfiles.views.needs_entry', name='needs_entry'),
    url(r'^political-files/edit/{}/add-spot/$'.format(uuid_re_str), 'fccpublicfiles.views.edit_related_politicalspot', name='add_related_politicalspot'),
    url(r'^political-files/edit/{}/edit-spot/(?P<spot_id>\d+)/$'.format(uuid_re_str), 'fccpublicfiles.views.edit_related_politicalspot', name='edit_related_politicalspot'),
    url(r'^political-files/edit/{}/$'.format(uuid_re_str), 'fccpublicfiles.views.politicalbuy_edit', name='politicalbuy_edit'),
    url(r'^political-files/add/advertiser/$', 'fccpublicfiles.views.add_advertiser', name='add_advertiser'),
    url(r'^political-files/add/advertiser_signatory/$', 'fccpublicfiles.views.add_advertiser_signatory', name='add_advertiser_signatory'),
    url(r'^political-files/add/media-buyer/$', 'fccpublicfiles.views.add_media_buyer', name='add_media_buyer'),
    url(r'^political-files/{}/$'.format(uuid_re_str), 'fccpublicfiles.views.politicalbuy_view', name='politicalbuy_view'),
    url(r'^political-files/broadcaster/(?P<callsign>[\w-]+)/$', broadcaster_views.broadcaster_detail,
        {'template_name': 'broadcaster_politicalbuys.html'}, name='broadcaster_politicalbuys_view'),
    url(r'^political-files/ajax/{}/spots/$'.format(uuid_re_str), 'fccpublicfiles.views.related_spots_ajax', name='related_spots_ajax'),
    url(r'^political-files/states/$', 'fccpublicfiles.views.state_fcc_list', name='state_list'),
    url(r'^political-files/dmas/$', 'fccpublicfiles.views.dma_fcc_list', name='dma_fcc_list'),
    url(r'^political-files/recent/states/$', 'fccpublicfiles.views.recent_state_fcc_list', name='recent_state_fcc_list'),
    url(r'^political-files/recent/dmas/$', 'fccpublicfiles.views.recent_dma_fcc_list', name='recent_dma_fcc_list'),
#    url(r'^political-files/stations/$', 'fccpublicfiles.views.station_fcc_list', name='station_fcc_list'),
    url(r'^political-files/stations/state/(?P<state_id>\w{2})/$', 'fccpublicfiles.views.station_state_list', name='station_state_list'),
    url(r'^political-files/stations/dma/(?P<dma_id>\d+)/$', 'fccpublicfiles.views.station_dma_list', name='station_dma_list'),
    url(r'^political-files/dma/(?P<dma_id>\d+)/$', 'fccpublicfiles.views.filing_dma_list', name='filing_dma_list'),
    url(r'^political-files/state/(?P<state_id>\w{2})/$', 'fccpublicfiles.views.filing_state_list', name='filing_state_list'),
    url(r'^political-files/tv-station/(?P<callsign>[\w\-]+)/$', 'fccpublicfiles.views.filing_station_list', name='filing_station_list'),
    url(r'^political-files/most-recent/', 'fccpublicfiles.views.fcc_most_recent', name='fcc_most_recent'),
    url(r'^political-files/advertisers/', 'fccpublicfiles.views.advertiser_list', name='advertiser_list'),  
    url(r'^political-files/advertiser/[\w-]+/(?P<advertiser_pk>\d+)/$', 'fccpublicfiles.views.advertiser_detail', name='advertiser_detail'),      
)
