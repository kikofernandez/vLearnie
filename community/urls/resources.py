from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index

# public urls
urlpatterns = patterns('',
        
    url(r'^$', 
        'community.views.communities.resume_index', 
        name='community_archive_index'),
        
    url(r'^(?P<year>\d{4})/$',
        'community.views.communities.show_resources_by_year',
        name='community_community_archive_year'),
        
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'community.views.communities.show_resources_by_month',
        name='community_community_archive_month'),
        
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'community.views.communities.show_resources_by_day',
        name='community_community_archive_day'),
        
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'community.views.communities.show_object_resource_details',
        name='community_community_details'),
)