from django.conf.urls import patterns, include, url
from .views import ActionSignupView

urlpatterns = patterns('',
    url(r'^action_signup/', ActionSignupView.as_view(), name='action_signup'),
    url(r'^accounts/register/$', 'volunteers.views.register_volunteer', name='register_volunteer'),
    url(r'^accounts/profile/$', 'volunteers.views.profile', name='profile'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
