from django.conf.urls.defaults import *

# public urls
urlpatterns = patterns('',
#    url(r'^$',
#      'community.views.communities.community_index',
#      name='community_index_communities'),
    url(r'^$',
        'community.views.communities.list_communities_public',
        name='community_public_list_communities'),
    
    url(r'^search/$',
        'community.views.communities.search',
        name="community_search"), 
     
    (r'^(?P<community>[-\w]+)/', include('community.urls.resources')),
)