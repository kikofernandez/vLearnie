from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

BLOG = ('wordpress', 'blogger', 'livejournal', 'feed')
SOCIAL = ('twitter', 'facebook', 'myspace', 'linkedin')
VIDEO = ('vimeo', 'youtube')
NEWS = ('delicious', 'digg', 'reddit', 'technorati', 'newsvine')
PHOTOS = ('flickr', 'picasa')
DASHBOARDS = ('netvibes', 'stumbleupon')
MUSIC = ('lastfm',)

message = 'Enter a valid %s link'

class SocialMediaReference(models.Model):
    SOCIAL_LINKS = (
        ('Blog', BLOG),
        ('Social', SOCIAL),
        ('Videos', VIDEO),
        ('News', NEWS),
        ('Photos', PHOTOS),
        ('Dashboards', DASHBOARDS),
        ('Music', MUSIC),
    )
    user = models.ForeignKey(User)
    
    twitter = models.URLField(validators=[RegexValidator('http://twitter\.com/.*',
                                                       message="Enter a valid twitter link.")],
                             blank=True)
    facebook = models.URLField(validators=[RegexValidator('http://www\.facebook.+',
                                                       message=message % 'facebook')],
                              blank=True)
    linkedin = models.URLField(blank=True,
                               validators=[RegexValidator('.+linkedin.+',
                                                          message=message % "linkedin")])
    skype = models.CharField(blank=True,
                             max_length=200)
    
    wordpress = models.URLField(blank=True,
                                validators=[RegexValidator('.+wordpress.+',
                                                           message=message % 'wordpress')])
    blogger = models.URLField(blank=True,
                              validators=[RegexValidator('.+blogpost.+',
                                                         message=message % 'blogger')])
    delicious = models.URLField(blank=True,
                                validators=[RegexValidator('.+delicious.+',
                                                         message=message % 'delicious')])
    digg = models.URLField(blank=True,
                           validators=[RegexValidator('.+digg.+',
                                                         message=message % 'digg')])
    feed = models.URLField(blank=True,
                           validators=[RegexValidator('.+feed.+',
                                                         message=message % 'feed')])
    flickr = models.URLField(blank=True,
                             validators=[RegexValidator('.+flickr.+',
                                                         message=message % 'flickr')])
    lastfm = models.URLField(blank=True,
                             validators=[RegexValidator('.+lastfm.+',
                                                         message=message % 'lastfm')])
    livejournal = models.URLField(blank=True,
                                  validators=[RegexValidator('.+livejournal.+',
                                                         message=message % 'live journal')])
    myspace = models.URLField(blank=True,
                              validators=[RegexValidator('.+myspace.+',
                                                         message=message % 'myspace')])
    netvibes = models.URLField(blank=True,
                               validators=[RegexValidator('.+netvibes.+',
                                                         message=message % 'netvibes')])
    newsvine = models.URLField(blank=True,
                               validators=[RegexValidator('.+newvine.+',
                                                         message=message % 'newsvine')])
    picasa = models.URLField(blank=True,
                             validators=[RegexValidator('.+picasa.+',
                                                         message=message % 'picasa')])
    reddit = models.URLField(blank=True,
                             validators=[RegexValidator('.+reddit.+',
                                                         message=message % 'reddit')])
    stumbleupon = models.URLField(blank=True,
                                  validators=[RegexValidator('.+stumbleupon.+',
                                                         message=message % 'stumbleupon')])
    technorati = models.URLField(blank=True,
                                 validators=[RegexValidator('.+technorati.+',
                                                         message=message % 'technorati')])
    vimeo = models.URLField(blank=True,
                            validators=[RegexValidator('.+vimeo.+',
                                                         message=message % 'vimeo')])
    youtube = models.URLField(blank=True,
                              validators=[RegexValidator('.+youtube.+',
                                                         message=message % 'youtube')])
    
    mail = models.EmailField(blank = True)
    
    def __unicode__(self):
        return "Social Media Reference for %s" % self.user