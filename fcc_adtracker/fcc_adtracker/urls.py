from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from fcc_adtracker.views import HomePageView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^broadcasters/', include('broadcasters.urls')),
    url(r'', include('sfapp.urls')),
    url(r'^$', HomePageView.as_view(), name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
