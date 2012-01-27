from django.conf.urls.defaults import *
#from coltrane.models import Entry

#entry_info_dict = {'queryset' : Entry.live.all(),'date_field' : 'pub_date',}

urlpatterns = patterns('',
    
    url(r'^$',
        'coltrane.views.main_area',
        name="space_space_main_area"),
    
    url(r'^search/$',
        'coltrane.views.search',
        name='search'),

    url(r'^(?P<username>[-\w]+)/$',
     'coltrane.views.show_spaces_by_username',
     name='coltrane_entry_archive_index_space'),
     
    url(r'^(?P<username>[-\w]+)/(?P<spacename>[-\w]+)/$',
     'coltrane.views.show_content_by_space_username',
     name='space_public_space_detail'),
     
    url(r'^(?P<username>[-\w]+)/(?P<spacename>[-\w]+)/blog/',
     include('coltrane.public_urls.entries')), 
     
    url(r'^(?P<username>[-\w]+)/(?P<spacename>[-\w]+)/links/',
     include('coltrane.public_urls.links')), 
     
    url(r'^(?P<username>[-\w]+)/(?P<spacename>[-\w]+)/categories/',
     include('coltrane.public_urls.categories')),
    
    url(r'^(?P<username>[-\w]+)/(?P<spacename>[-\w]+)/tags/',
     include('coltrane.public_urls.tags')),
)