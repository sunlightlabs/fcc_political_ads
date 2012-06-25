from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from fcc_adtracker.views import HomePageView
from ajax_select import urls as ajax_select_urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^broadcasters/', include('broadcasters.urls')),
    url(r'^volunteers/', include('volunteers.urls')),
    # url(r'^publicfiles/', include('fccpublicfiles.urls')),
    url(r'', include('sfapp.urls')),
    url(r'^$', 'broadcasters.views.featured_broadcasters', name='home'),
    
    # url(r'autocomplete/', include('autocomplete_light.urls')),
    (r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/fccpublicfiles/', include('fccpublicfiles.admin_urls')),
    url(r'^admin/', include(admin.site.urls)),
)
