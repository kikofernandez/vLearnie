from django.contrib.auth.models import User
from django.db import models
#from coltrane.models import Category as CategoryPlugin
#from coltrane.models import Entry
#
#class Category(CategoryPlugin):
#    space = models.ForeignKey(Entry)
#    
#    class Meta:
#        unique_together = ((''))


class Space(models.Model):
    """
    This will link the User with a title.
    The id (created automagically) is the PK.
    We want the user and slug to be unique, so we define it in the Meta class. 
    The URL will be: www.XXX.yy/space/yourname/slug/
    """
    user = models.ForeignKey(User)
    title = models.CharField(max_length="30",
                             help_text="This will be the name of your space")
    slug = models.SlugField(#unique=True,
                            help_text="Automatically generated from title")
    
    class Meta:
        unique_together = (('user', 'slug'))
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        #return "/space/%s/%s/" % (self.user.username, self.slug)
        return ('space_public_space_detail',
                (),
                {'username': self.user.username,
                 'spacename': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)