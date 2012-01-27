import datetime  

from django.db import models
from django.contrib.auth.models import User

from tagging.fields import TagField
from markdown import markdown

from django.db.models.base import get_absolute_url

from django.db.models import signals
from django.contrib.comments import Comment

from coltrane.signals import moderate_comment
#from community.signals import create_resource, update_m2m_resource
from community.models import Resource, Community
from space.models import Space
from markdown import markdown
#class LiveTagManager(models.Manager):
#    def get_query_set(self):
#        return super(LiveTagManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Category(models.Model):
    space = models.ForeignKey(Space)
    title = models.CharField(max_length=250,
                             help_text='Maximum 250 characters')
    author = models.ForeignKey(User)
    slug = models.SlugField(#unique=True,
                            help_text='Suggested value generated automatically from title. Must be unique')
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)
    
    def live_entry_set(self):
        #from coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"
        unique_together = (('space', 'slug'),)
    
    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.description_html = markdown(self.description)
        super(Category, self).save(force_insert, force_update)
    
    def get_absolute_url(self):
        #return "/weblog/categories/%s/" % self.slug
        
        return ('coltrane_category_detail',
                (),
                {'username': self.author,
                 'spacename': self.space,
                 'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    
class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

def get_current_date():
        return datetime.date.strftime(datetime.date.today(), "%Y-%m-%d")

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    
    #Managers
    # It seems that the order of the Managers matters. You write live above objects and
    # you won't see the draft or hidden entries.
    objects = models.Manager()
    live = LiveEntryManager()
    #objects = models.Manager()
    
    #core fields
    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True,
                               help_text='This field is optional.')
    body = models.TextField()
    #pub_date = models.DateField(default=datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d"))
    pub_date = models.DateField(default=datetime.date.today)
    #pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    # fields to storage generated HTML
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)
    
    #Metadata
    space = models.ForeignKey(Space)
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    #post_elsewhere = models.BooleanField(default=False)
    slug = models.SlugField(#unique_for_date='pub_date',
                            help_text="Suggested value automatically generated from title. Must be unique")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS,
                                 help_text="Only entries with live status will be publicly displayed")
    
    # Categorazation
    categories = models.ManyToManyField(Category)
    tags = TagField(help_text="Separate tags with spaces")
    
    community = models.ForeignKey(Community, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']
        unique_together = (('author', 'space', 'pub_date', 'slug'),)
    
    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update)
    
    def get_absolute_url(self):
        #return "/weblog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
        return ('coltrane_entry_detail',
                (),
                {'username': self.author.username,
                 'spacename': self.space.slug,
                 'year' : self.pub_date.strftime("%Y"),
                 'month' : self.pub_date.strftime("%b").lower(),
                 'day' : self.pub_date.strftime("%d"),
                 'slug' : self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def allow_comments(self):
        if (datetime.date.today() - self.pub_date).days > 30:
            return False
        return True
   
   
class Link(models.Model):
    #Metadata
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to delicious', default=True)
    posted_by = models.ForeignKey(User)
    space = models.ForeignKey(Space)
    pub_date = models.DateField(default=datetime.date.today)
    slug = models.SlugField()
    title = models.CharField(max_length=250)
    
    # The actual link bits
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True, editable=False)
    url = models.URLField()
    tags = TagField()
    via_name = models.CharField('Via', max_length=250, blank=True,
                                help_text='The name of the person whose site you spotted the link on. Optional')
    via_url = models.URLField('Via URL', blank=True,
                              help_text='The URL of the site where you spotted the link. Optional')
    
    class Meta:
        ordering = ['-pub_date']
        unique_together = (('space', 'posted_by', 'pub_date','slug'),)
    
    def __unicode__(self):
        return self.title
    
    def save(self):
        if self.description:
            self.description_html = markdown(self.description)
        super(Link, self).save()
        
    def get_absolute_url(self):
        return ('coltrane_link_detail',
                (), 
                {'username': self.posted_by.username,
                 'spacename': self.space.slug,
                 'year' : self.pub_date.strftime("%Y"),
                 'month' : self.pub_date.strftime("%b").lower(),
                 'day' : self.pub_date.strftime("%d"),
                 'slug' : self.slug})
#                {'year': self.pub_date.strftime('%Y'),
#                 'month': self.pub_date.strftime("%b").lower(),
#                 'day': self.pub_date.strftime("%d"),
#                 'slug': self.slug})
    
    get_absolute_url = models.permalink(get_absolute_url) 



# Signals
         
signals.pre_save.connect(moderate_comment, sender=Comment)
#signals.post_save.connect(manage_resource, sender=Entry)
#signals.post_save.connect(create_resource, sender=Entry)
#signals.m2m_changed.connect(update_m2m_resource, sender=Entry.community.through, weak=False)