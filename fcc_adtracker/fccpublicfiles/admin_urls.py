from django.conf.urls import patterns, include, url


urlpatterns = patterns('fccpublicfiles',
    url(r'^field_json/', 'views.admin_autocomplete_json', name='admin_autocomplete_json'),
)
