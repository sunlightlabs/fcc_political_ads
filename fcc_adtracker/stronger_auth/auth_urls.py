from django.conf.urls import patterns, url

from stronger_auth.forms import TougherSetPasswordForm, TougherChangePasswordForm

urlpatterns = patterns('',
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
        {'password_change_form': TougherChangePasswordForm}),
    url(r'^password_changed/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'set_password_form': TougherSetPasswordForm}),
)
