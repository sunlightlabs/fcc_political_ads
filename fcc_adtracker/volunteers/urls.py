from django.conf.urls import patterns, include, url
from .views import ActionSignupView

urlpatterns = patterns('volunteers',
    url(r'^action_signup/', ActionSignupView.as_view(), name='action_signup'),
)
