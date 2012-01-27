from django.conf.urls.defaults import *
from piston.resource import Resource
from api.coltrane.handlers import BlogPostHandler, DefaultBlogPostHandler
from piston.authentication import HttpBasicAuthentication
from api.csrfexempt import CsrfExemptResource

auth = HttpBasicAuthentication(realm="My sample API")
blogpost_handler = CsrfExemptResource(BlogPostHandler, authentication = auth)
default_blogpost_handler = CsrfExemptResource(DefaultBlogPostHandler, authentication = auth)

urlpatterns = patterns('',
    url(r'^$',
        default_blogpost_handler, 
        {'emitter_format': 'json'}),
    
    url(r'^(?P<id>\d+)/$',
        default_blogpost_handler, 
        {'emitter_format': 'json'}),
    
    url(r'^(?P<author>[-\w]+)/$', 
        blogpost_handler, 
        {'emitter_format': 'json'}),
    
    url(r'^(?P<author>[-\w]+)/(?P<space>\d+)/$', 
        blogpost_handler, 
        {'emitter_format': 'json'}),
        
#    url(r'^(?P<author>\d+)/(?P<space>[-\w]+)/(?P<pub_date>.+)/$',
#        blogpost_handler,
#        {'emitter_format': 'json'}),
    
    url(r'^(?P<author>[-\w]+)/(?P<space>\d+)/(?P<pub_date>[-\d]+)/$',
        blogpost_handler,
        {'emitter_format': 'json'}),
    
    url(r'^(?P<id>\d+)/(?P<emitter_format>\w+)/$',
        default_blogpost_handler),
        
    url(r'^(?P<author>[-\w]+)/(?P<emitter_format>\w+)/$',
        blogpost_handler),
    
    url(r'^(?P<author>[-\w]+)/(?P<space>\d+)/(?P<emitter_format>\w+)/$',
        blogpost_handler),
    
    url(r'^(?P<author>[-\w]+)/(?P<space>\d+)/(?P<pub_date>[-\d]+)/(?P<emitter_format>\w+)/$',
        blogpost_handler),
         
#    url(r'^(?P<author>[-\w]+)/(?P<space>\d+)/$', 
#        blogpost_handler, 
#        {'emitter_format': 'json'}),
#        
#    url(r'^(?P<author>[-\w]+)/(?P<space>\d+)/(?P<emitter_format>.+)/$',
#        blogpost_handler),
        
#    url(r'^(?P<author>[-\w]+)/(?P<emitter_format>.+)/$',
#        blogpost_handler,
#        {'emitter_format': 'json'}),
    
#    url(r'^(?P<author>[-\w]+)/$', 
#        blogpost_handler, 
#        {'emitter_format': 'json'}),
    
#    url(r'^$',
#        default_blogpost_handler, 
#        {'emitter_format': 'json'}),  
)