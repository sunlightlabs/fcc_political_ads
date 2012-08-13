from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from fcc_adtracker.views import HomePageView
from ajax_select import urls as ajax_select_urls

from django.contrib import admin
import moderation.helpers

moderation.helpers.auto_discover()
admin.autodiscover()


urlpatterns = patterns('',
    # url(r'^broadcasters/', include('broadcasters.urls')),
    url(r'', include('volunteers.urls')),
    url(r'', include('fccpublicfiles.urls')),
    url(r'', include('sfapp.urls')),
    url(r'^$', 'fccpublicfiles.views.featured_broadcasters', name='home'),
    (r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
