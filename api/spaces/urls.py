from api.spaces.handlers import SpaceHandler 
from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from api.csrfexempt import CsrfExemptResource

auth = HttpBasicAuthentication(realm="My sample API")
space_handler = CsrfExemptResource(SpaceHandler, authentication = auth)

urlpatterns = patterns('',
    url(r'^$',
        space_handler,
        {'emitter_format':'json'}),
    
    url(r'^(?P<id>\d+)/$',
        space_handler,
        {'emitter_format':'json'}),
    
    url(r'^(?P<emitter_format>[\w]+)/$',
        space_handler),
    
    url(r'^(?P<id>\d+)/(?P<emitter_format>[\w]+)/$',
        space_handler),
)