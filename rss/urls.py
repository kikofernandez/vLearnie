from django.conf.urls.defaults import *
from rss.feeds import LatestEntriesFeedRSS, LatestEntriesFeedByCategoryRSS,\
    CommunityEntryRss, CommunityEntryAtom


feeds = {'entries': LatestEntriesFeedRSS,
         #'communities': LatestCommunitiesEntriesFeedRSS
         }

urlpatterns = patterns('',
    
    url(r'^community/(?P<community_name>[-\w]+)/rss/$',
     CommunityEntryRss(),
     name="community_rss"),
    
    url(r'^community/(?P<community_name>[-\w]+)/atom/$',
     CommunityEntryAtom(),
     name="community_atom"),
    
#    (r'^community/(?P<community_name>[-\w]+)/rss/$',
#        LatestCommunitiesEntriesFeedRSS()),
    
    (r'^(?P<user_name>[-\w]+)/(?P<spacename>[-\w]+)/(?P<id>[\d]+)/rss/$',
        LatestEntriesFeedRSS()),
    (r'^(?P<user_name>[-\w]+)/(?P<spacename>[-\w]+)/category/(?P<id>[\d]+)/rss/$',
        LatestEntriesFeedByCategoryRSS()),
                       
#    (r'^(?P<url>.*)/$',
#     'django.contrib.syndication.views.feed',
#     {'feed_dict': feeds}),
)