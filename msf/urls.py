from django.conf.urls.defaults import *
from msf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    # (r'^msf/', include('msf.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^space/', include('coltrane.public_urls.spaces')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/', include('rss.urls')),
    url(r'^form/moodle/$', 'form.views.redirect_to_login_moodle', name='redirecto_moodle'),
    (r'^form/$', 'form.views.getsessionid'),
    url(r'^form/logout/$', 'form.views.logout_request', name="logout"),
    (r'^profile/', include('login.urls')),
    (r'^account/friendlist/', include('friendycontrol.urls')),
    (r'^account/community/', include('community.urls.admin_url')),
    (r'^account/spaces/', include('space.urls')),
    (r'^account/portfolio/', include('portfolio.urls.admin')),
    (r'^media/(?P<path>.*)$', 
     'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT },
     'media_url'),
    
    (r'^portfolio/', include('portfolio.urls.public')),
    (r'^community/', include('community.urls.urls')),
    (r'^validator/', include('output_validator.urls')),
    # API providing web services
    (r'^api/blog/', include('api.coltrane.urls')),
    (r'^api/community/', include('api.community.urls')),
    (r'^api/fhy/', include('api.fhy.urls')),
    (r'^api/portfolio/', include('api.portfolio.urls')),
    (r'^api/space/', include('api.spaces.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
