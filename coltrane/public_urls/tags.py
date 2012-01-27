from django.conf.urls.defaults import *
from tagging.models import Tag
from coltrane.models import Entry, Link

urlpatterns = patterns('',
    url(r'^$',
     'coltrane.views.show_tag_index',   
     name='coltrane_tag_list'),
     
#    url(r'^entries/(?P<tag>[\w-]+)/$',
#        'coltrane.views.show_tagged_object_list',
#        name='coltrane_entries_tagged'),

    url(r'^entries/(?P<tag>\d+)/$',
        'coltrane.views.show_tagged_object_list',
        name='coltrane_entries_tagged'),

#    url(r'^links/(?P<tag>[\w-]+)/$',
#        'coltrane.views.show_tagged_links_object_list',
#        name='coltrane_links_tagged')

    url(r'^links/(?P<tag>\d+)/$',
        'coltrane.views.show_tagged_links_object_list',
        name='coltrane_links_tagged')
)
