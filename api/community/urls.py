from django.conf.urls.defaults import *
from piston.resource import Resource
from api.community.handlers import CommunityHandler, ResourceHandler, DefaultResourceHandler
from piston.authentication import HttpBasicAuthentication
from api.csrfexempt import CsrfExemptResource

auth = HttpBasicAuthentication(realm="My sample API")
community_handler = CsrfExemptResource(CommunityHandler, authentication = auth)
resource_handler = CsrfExemptResource(ResourceHandler, authentication = auth)
default_resource_handler= CsrfExemptResource(DefaultResourceHandler, authentication = auth)

urlpatterns = patterns('',
                       
    url(r'^(?P<id>\d+)/$',
        community_handler,
        {'emitter_format':'json'}),
    
    url(r'^(?P<id>\d+)/resources/$',
        resource_handler,
        {'emitter_format':'json'}),
    
    url(r'^(?P<id>\d+)/resources/(?P<resource_id>\d+)/$',
        resource_handler,
        {'emitter_format':'json'}),
    
    url(r'^resource/$',
        default_resource_handler,
        {'emitter_format':'json'}),
    
    url(r'^resource/(?P<id>\d+)/$',
        default_resource_handler,
        {'emitter_format':'json'}),
    
    
    url(r'^(?P<id>\d+)/resources/(?P<emitter_format>\w+)/$',
        resource_handler),
    
    url(r'^resource/(?P<emitter_format>\w+)/$',
        default_resource_handler,),
    
    url(r'^resource/(?P<id>\d+)/(?P<emitter_format>\w+)/$',
        default_resource_handler),
    
    url(r'^(?P<id>\d+)/(?P<emitter_format>\w+)/$',
        community_handler),
    
    url(r'^(?P<emitter_format>\w+)/$',
        community_handler),
    
    
    url(r'$',
        community_handler,
        {'emitter_format':'json'}),
    
    
#    url(r'^resource/$',
#        default_resource_handler,
#        {'emitter_format':'json'}),
#    
#    url(r'^resource/(?P<id>\d+)/$',
#        default_resource_handler,
#        {'emitter_format':'json'}),
    
#    url(r'^(?P<emitter_handler>.+)/$',
#        community_handler),
        
#    url(r'$',
#        community_handler,
#        {'emitter_format':'json'}),
)