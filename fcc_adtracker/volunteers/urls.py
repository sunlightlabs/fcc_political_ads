from django.conf.urls import patterns, include, url
from .views import ActionSignupView

urlpatterns = patterns('',
    url(r'^action_signup/', ActionSignupView.as_view(), name='action_signup'),
    url(r'^account/register/$', 'volunteers.views.register_volunteer', name='register_volunteer'),
    url(r'^account/profile/$', 'volunteers.views.profile', name='profile'),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^account/', include('registration.backends.default.urls')),
    url(r'', include('social_auth.urls')),
)
