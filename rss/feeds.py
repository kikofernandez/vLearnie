from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.contrib.sites.models import Site
#from django.contrib.syndication.feeds import Feed as FeedsFeed
from django.contrib.syndication.views import Feed
from coltrane.models import Entry, Category
from community.models import Resource, Community
from django.shortcuts import get_object_or_404

current_site = Site.objects.get_current()

def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]+suffix

class CommunityEntryRss(Feed):
    feed_type = Rss201rev2Feed
    
    def get_object(self, request, community_name):
        return get_object_or_404(Community, slug=community_name)
    
    def title(self, obj):
        return "Entries in community: %s" % obj.title
    
    def description(self, obj):
        return "Description of this community: %s" % obj.title
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def items(self, obj):
        return Resource.live.filter(community__id=obj.id)
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.body
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_author_name(self, item):
        return item.author.username
    
    def item_pubddate(self, item):
        return item.pubdate

class CommunityEntryAtom(CommunityEntryRss):
    feed_type = Atom1Feed
    
    def subtitle(self, obj):
        return "Description of this community: %s" % obj.title
    
    def item_subtitle(self, item):
        return item.body

#class LatestCommunitiesEntriesFeedRSS(Feed):
##    feed_type = Atom1Feed
#    feed_type = Rss201rev2Feed
#    
#    def get_object(self, request, community_name):
#        return get_object_or_404(Community.objects, slug=community_name)
#        #Entry.live.filter(author__username=username).filter(space__slug=spacename)
#    
#    def title(self, obj):
#        return obj.title
#    
#    def link(self, obj):
#        return obj.get_absolute_url()
#    
#    def description(self, obj):
#        if obj.excerpt:
#            return obj.excerpt
#        return smart_truncate(obj.description, 100, '...')
#    
#    def subtitle(self, obj):
#        if obj.excerpt:
#            return obj.excerpt
#        return smart_truncate(obj.description, 100, '...')
#    
#    def items(self, obj):
#        return Resource.objects.all()[:15]
#        #return Resource.objects.live_resources(community__slug=obj.community_name)[:15]
#    
#    def item_title(self, item):
#        return item.title
#    
##    def item_pubdate(self, item):
##        return item.pub_date
#    
##    def item_categories(self, item):
##        return [c.title for c in item.categories.all()]
#    
#    def item_description(self, item):
#        if item.excerpt:
#            return item.excerpt
#        return smart_truncate(item.description, 100, '...')

class LatestEntriesFeedRSS(Feed):
#    feed_type = Atom1Feed
    feed_type = Rss201rev2Feed
    
    def get_object(self, request, user_name, spacename, id):
        return get_object_or_404(Entry.live, author__username=user_name,
                                             space__slug=spacename,
                                             id = id)
        #Entry.live.filter(author__username=username).filter(space__slug=spacename)
    
    def title(self, obj):
        return obj.body
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        if obj.excerpt:
            return obj.excerpt
        return smart_truncate(obj.body, 100, '...')
    
    def subtitle(self, obj):
        if obj.excerpt:
            return obj.excerpt
        return smart_truncate(obj.body, 100, '...')
    
    def items(self, obj):
        return Entry.live.filter(author=obj.author).filter(space=obj.space)[:15]
    
    def item_title(self, item):
        return item.title
    
#    def item_pubdate(self, item):
#        return item.pub_date
    
    def item_categories(self, item):
        return [c.title for c in item.categories.all()]
    
    def item_description(self, item):
        if item.excerpt:
            return item.excerpt
        return smart_truncate(item.body, 100, '...')

class LatestEntriesFeedByCategoryRSS(LatestEntriesFeedRSS):
    def get_object(self, request, user_name, spacename, id):
        return get_object_or_404(Category, author__username = user_name,
                                           space__slug=spacename,
                                           id=id)
    
    def title(self, obj):
        return obj.title
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        return smart_truncate(obj.description, 50, '...')
    
    def subtitle(self, obj):
        return smart_truncate(obj.description, 50, '...')
    
    def items(self, obj):
        return obj.live_entry_set()[:15]


#class LatestEntriesFeed(FeedsFeed):
#    author_name = "Kiko"
#    subtitle = "Latest entries posted to %s" % current_site.name
#    feed_type = Atom1Feed
#    link = "/feeds/entries/"
#    title = "%s: Latest entries" % current_site.name
#    
#    def items(self):
#        return Entry.live.all()[:10]
#    
#    def item_pubdate(self, item):
#        return item.pub_date
#    
#    def item_categories(self, item):
#        return [c.title for c in item.categories.all()]
#    
#    def item_guid(self ,item):
#        return "tag:%s,%s:%s" % (current_site.domain,
#                                 item.pub_date.strftime('%Y-%m-%d'),
#                                 item.get_absolute_url())
#        
#class CategoryFeed(LatestEntriesFeed):
#    def get_object(self, bits):
#        if len(bits)!=1:
#            raise ObjectDoesNotExist
#        return Category.objects.get(slug__exact=bits[0])
#    
#    def title(self, obj):
#        return "%s: Latest entries in category '%s'" % (current_site.name,
#                                                        obj.title)
#    def description(self, obj):
#        return "%s: Latest entries in category '%s'" % (current_site.name,
#                                                        obj.title)
#    def link(self, obj):
#        return obj.get_absolute_url()
#    
#    def items(self, obj):
#        return obj.live_entry_set()[:15]