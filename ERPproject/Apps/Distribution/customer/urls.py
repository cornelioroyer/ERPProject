__author__ = 'FARID ILHAM Al-Q'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'profile/$', 'Apps.Distribution.customer.views.profile'),
                       url(r'update/$', 'Apps.Distribution.customer.views.update_profile'),
                       url(r'register/$', 'Apps.Distribution.customer.views.registration'),
                       url(r'success/$', 'Apps.Distribution.customer.views.registration_success'),
                       url(r'login/$', 'Apps.Distribution.customer.views.login_request'),
                       url(r'logout/$', 'Apps.Distribution.customer.views.logout_request'),
                       url(r'logged_out/$', 'Apps.Distribution.customer.views.logout_success'),
                       url(r'username_change/$', 'Apps.Distribution.customer.views.username_change'),
                       url(r'^password_change/$', 'Apps.Distribution.customer.views.password_change', name='password_change'),
                       url(r'^password_change/done/$', 'Apps.Distribution.customer.views.password_change_done',
                           name='password_change_done'),
                       url(r'^password_reset/$', 'Apps.Distribution.customer.views.password_reset', name='password_reset'),
                       url(r'^password_reset/done/$', 'Apps.Distribution.customer.views.password_reset_done',
                           name='password_reset_done'),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           'Apps.Distribution.customer.views.p'
                           'assword_reset_confirm',
                           name='password_reset_confirm'),
                       url(r'^reset/done/$', 'Apps.Distribution.customer.views.password_reset_complete',
                           name='password_reset_complete'),
                       url(r'^reset_password/password_sent/$','django.contrib.auth.views.password_reset_done'),
                       url(r'^reset_password/$','django.contrib.auth.views.password_reset'),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm'),
                       url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete'),

)
