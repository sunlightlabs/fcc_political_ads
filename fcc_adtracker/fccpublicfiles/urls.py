from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from fcc_adtracker.views import HomePageView
from ajax_select import urls as ajax_select_urls
from fccpublicfiles.views import prelim_doc_form

from django.contrib import admin
import moderation.helpers

moderation.helpers.auto_discover()
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/fccpublicfiles/', include('fccpublicfiles.admin_urls')),
    url(r'^document/submit/', 'fccpublicfiles.views.prelim_doc_form', name='document_submit'),
    url(r'^document/success/', 'fccpublicfiles.views.doc_success', name='document_success'),
    url(r'^politicalbuy/edit/(?P<buy_id>\d+)/', 'fccpublicfiles.views.politicalbuy_edit', name='politicalbuy_edit'),
)

