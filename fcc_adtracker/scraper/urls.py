from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('scraper.views',
#    url(r'^states/$', 'state_fcc_list', name='state_fcc_list'),
#    url(r'^dmas/$', 'dma_fcc_list', name='dma_fcc_list'),
#    url(r'^recent/states/$', 'recent_state_fcc_list', name='recent_state_fcc_list'),
#    url(r'^recent/dmas/$', 'recent_dma_fcc_list', name='recent_dma_fcc_list'),
#    url(r'^stations/$', 'station_fcc_list', name='station_fcc_list'),    
#    url(r'^stations/state/(?P<state_id>\w{2})/$', 'station_state_list', name='station_state_list'),
#    url(r'^stations/dma/(?P<dma_id>\d+)/$', 'station_dma_list', name='station_dma_list'),
#    url(r'^by-dma/(?P<dma_id>\d+)/$', 'filing_dma_list', name='filing_dma_list'),
#    url(r'^by-state/(?P<state_id>\w{2})/$', 'filing_state_list', name='filing_state_list'),
#    url(r'^by-tv-station/(?P<callsign>[\w\-]+)/$', 'filing_station_list', name='filing_station_list'),
#    url(r'^most-recent/', 'fcc_most_recent', name='fcc_most_recent'),
    url(r'^r/(?P<buy_id>\d+)/', 'ad_buy_redirect', name='ad_buy_redirect'),
    )