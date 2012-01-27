from django.conf.urls.defaults import *
from piston.resource import Resource
from api.fhy.handlers import FHYRootHandler, FHYFileHandler, FHYImageHandler, \
    DefaultFileHandler, FHYFileRemoverHandler, FHYImageRemoverHandler, DefaultFileHandler, DefaultImageHandler
from piston.authentication import HttpBasicAuthentication
from api.csrfexempt import CsrfExemptResource


auth = HttpBasicAuthentication(realm="My sample API")
#auth = HttpMSFAuthentication(realm="My sample API")
fhy_handler = CsrfExemptResource(FHYRootHandler, authentication = auth)
fhy_file_handler = CsrfExemptResource(FHYFileHandler, authentication = auth)
fhy_image_handler = CsrfExemptResource(FHYImageHandler, authentication = auth)
fhy_fileremover_handler = CsrfExemptResource(FHYFileRemoverHandler, authentication = auth)
fhy_imageremover_handler = CsrfExemptResource(FHYImageRemoverHandler, authentication = auth)
default_fhyfile_handler = CsrfExemptResource(DefaultFileHandler, authentication = auth)
default_fhyimage_handler = CsrfExemptResource(DefaultImageHandler, authentication = auth)


urlpatterns = patterns('',
    
    url(r'^delete_file/(?P<id>[\d]+)/$',
        fhy_fileremover_handler,
        {'emitter_format':'json'}),
    
    url(r'^delete_image/(?P<id>[\d]+)/$',
        fhy_imageremover_handler,
        {'emitter_format':'json'}),
        
    url(r'^file/$',
        default_fhyfile_handler,
        {'emitter_format':'json'}),
    
    url(r'^file/(?P<id>\d+)/$',
        default_fhyfile_handler,
        {'emitter_format':'json'}),
    
    url(r'^image/$',
        default_fhyimage_handler,
        {'emitter_format':'json'}),
    
    url(r'^image/(?P<id>\d+)/$',
        default_fhyimage_handler,
        {'emitter_format':'json'}),
    
    url(r'^(?P<space_id>\d+)/$',
        fhy_handler,
        {'emitter_format':'json'}),
    
    url(r'^(?P<username>[-\w]+)/files/$',
        fhy_file_handler,
        {'emitter_format':'json'}),
    
    url(r'^(?P<username>[-\w]+)/images/$',
        fhy_image_handler,
        {'emitter_format':'json'}),
    
    url(r'^delete_file/(?P<id>[\d]+)/(?P<emmiter_format>[-\w]+)/$',
        fhy_fileremover_handler),
    
    url(r'^delete_image/(?P<id>[\d]+)/(?P<emmiter_format>[-\w]+)/$',
        fhy_imageremover_handler),
        
    url(r'^file/(?P<emmiter_format>[-\w]+)/$',
        default_fhyfile_handler),
    
    url(r'^file/(?P<id>\d+)/(?P<emmiter_format>[-\w]+)/$',
        default_fhyfile_handler),
    
    url(r'^image/(?P<emmiter_format>[-\w]+)/$',
        default_fhyimage_handler),
    
    url(r'^image/(?P<id>\d+)/(?P<emmiter_format>[-\w]+)/$',
        default_fhyimage_handler),
    
    url(r'^(?P<space_id>\d+)/(?P<emitter_format>.+)/$',
        fhy_handler),
)