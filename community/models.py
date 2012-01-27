from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from django.db.models.base import get_absolute_url
from markdown import markdown
#from model_utils.managers import InheritanceManager
#from coltrane.models.Entry import STATUS_CHOICES

LIVE = 0
DRAFT = 1
HIDDEN = 2

class CommunityManager(models.Manager):
    def live_resources(self, community):
        return community.resource_set.filter(type=LIVE)

class Community(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(blank=True)
    excerpt_html = models.TextField(blank=True,
                                    editable=False)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True,
                                        editable=False)
    objects = CommunityManager()
    class Meta:
        verbose_name_plural = 'Communities'
    
    def get_absolute_url(self):
        return ('community_archive_index',
                (),
                {'community': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __unicode__(self):
        return self.slug
    
    def save(self, force_insert=False, force_update=False):
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        if self.description:
            self.description_html = markdown(self.description)
        super(Community, self).save(force_insert, force_update)
    
    def entries(self):
        return len(self.resource_set.all())
    
    def live_entries(self):
        return len(Community.objects.live_resources(self).all())
    
class LiveResourceManager(models.Manager):
    def get_query_set(self):
        return super(LiveResourceManager, self).get_query_set().filter(type=self.model.LIVE)

class Resource(models.Model):
    LIVE = 0
    STATUS_TYPE = (
        (LIVE, 'LIVE'),
        (DRAFT, 'DRAFT'),
        (HIDDEN, 'HIDDEN'),
    ) 

    community = models.ForeignKey(Community)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    slug = models.SlugField(unique_for_date='pub_date')
    pub_date = models.DateField()
    type = models.IntegerField(choices=STATUS_TYPE)
    excerpt = models.TextField(blank=True)
    excerpt_html = models.TextField(blank=True,
                                    editable=False)
    #objects = InheritanceManager()
    tags = TagField()
    body = models.TextField()
    body_html = models.TextField(blank=True,
                                 editable=False)
    
    # Managers
    objects = models.Manager()
    live = LiveResourceManager()
    
    def __unicode__(self):
        return "Entry: %s" % self.slug
    
    def save(self, force_insert=False, force_update=False):
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        self.body_html = markdown(self.body)
        super(Resource, self).save(force_insert, force_update)
    
    def get_absolute_url(self):
        return ('community_community_details',
                #'community_community_public_details',
                (),
                {'community': self.community,
                 'year': self.pub_date.strftime("%Y"),
                 'month': self.pub_date.strftime('%m'),
                 'day': self.pub_date.strftime('%d'),
                 'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)    
    
#    def get_absolute_url(self):
#        return ('community_community_details',
#                (),
#                {'community': self.community,
#                 'year': self.pub_date.strftime("%Y"),
#                 'month' : self.pub_date.strftime("%m"),
#                 'day' : self.pub_date.strftime("%d"),
#                 'slug' : self.slug})
#    get_absolute_url = models.permalink(get_absolute_url)

#class EntryCommunityResource(Resource):
#    body = models.TextField()
#    url_referrer = models.URLField()
#    tags = TagField()
#
#    
#    def __unicode__(self):
#        return "CommunityEntry: %s" % self.slug
    
#    def get_absolute_url(self):
#        return ('community_community_details',
#                (),
#                {'community': self.community.slug,
#                 'year': self.pub_date.strftime("%Y"),
#                 'month' : self.pub_date.strftime("%m"),
#                 'day' : self.pub_date.strftime("%d"),
#                 'slug' : self.slug})
#    get_absolute_url = models.permalink(get_absolute_url)


#class URLCommunityResource(Resource):
#    url_referrer = models.URLField()
#    tags = TagField()
#
#    
#    def __unicode__(self):
#        return "URLCommunity: %s" % self.url_referrer
    
#    def get_absolute_url(self):
#        return ('community_community_details',
#                (),
#                {'community': self.community,
#                 'year': self.pub_date.strftime("%Y"),
#                 'month' : self.pub_date.strftime("%m"),
#                 'day' : self.pub_date.strftime("%d"),
#                 'slug' : self.slug})
#    get_absolute_url = models.permalink(get_absolute_url)