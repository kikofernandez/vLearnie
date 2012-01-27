from django.conf.urls.defaults import *

urlpatterns = patterns('login.views',
    url(r'^account/$', 'profile', {}, 'session_profile'),
    #url(r'^logout/$', 'logout_view', {}, 'signup_signupform_logout'),
)