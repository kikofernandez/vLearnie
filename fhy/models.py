from django.db import models
from space.models import Space
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import permalink
from djangothumbs.thumbs import ImageWithThumbsField

import datetime
from msf import settings

#from django.core.files import File
#from django.contrib.auth.admin import User

# 1024 b * 1024 b = 1 Mb
MAX_FILE_SIZE = settings.FHY_MAX_FILE_SIZE

class Folder(models.Model):
    """
    This object represent a virtual folder. They have title, the URL to track it down, 
    and a GenericForeignKey so that it allows us to have a folder inside a folder and
    a folder that belongs to the Root object.
    
    **Arguments:**
        * id: AutoField
        * title: CharField
        * slug: SlugField
        * object_id: PositiveInteger
        * content_object: GenericForeignKey
        * space: :class:`Space <space.models.Space>`
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=25)
    slug = models.SlugField()
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()
    space = models.ForeignKey(Space)
    
#    Since we do not want two objects with the same URL for the same folder / root.
#    We assume the slugfield will be the Slugify title
# The second condition in meta ensures that there won't exist tweo objects
# with the same parent and identical slug. Therefore, two folders from the same parent
# with identical names.
    
    class Meta:
        #unique_together = (('id', 'slug', 'object_id'))
        unique_together = (('id', 'space'), ('space', 'object_id', 'slug', 'content_type'))
    
    def __unicode__(self):
        return "Folder object (%s, %s, %s, %s)" % (self.id, self.slug, 
                                                   self.content_type, self.object_id)

class AbstractFile(models.Model):
    """
    This class represent the relation of the file / image within the folder / root folder.
    Due to a File or Image can point to a Folder object or Root object, we need to use
    a GenericForeignKey.
    
    **Arguments:**
        * title: CharField
        * slug: SlugField
        * description: TextField
        * object_id: PositiveInteger
        * content_object: GenericForeignKey
        * space: :class:`Space <space.models.Space>`
    """
    title = models.CharField(max_length=15)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()
    space = models.ForeignKey(Space)
    pub_date = models.DateField(default=datetime.date.today)
    
    class Meta:
        abstract = True
        
class FileFHY(AbstractFile):
    """
    An File object. We can add new attributes related with dimensions, max size, etc
    
    **Arguments:**
        * file: :class:`FileField <django.db.models.FileField>`
    """
    file = models.FileField(upload_to='files/%Y/%m/%d')
    
    class Meta:
        verbose_name_plural = 'Files'
        unique_together = (('slug', 'object_id', 'space', 'content_type'))
    
    def __unicode__(self):
        return "File object (%s, %s)" % (self.title, self.file)
    
#    def get_absolute_url(self):
#        return ('public_folder_view', (), {'space': self.space.slug,
#                                           'object_id': self.object_id})
#    get_absolute_url = permalink(get_absolute_url)
        
    def set_location(self, location):
        file = self.file.__dict__.get('instance').__dict__.get('file')
        file.field.upload_to = location

class ImageFHY(AbstractFile):
    """
    An Image object. We can add new attributes related with dimensions, max size, etc
    
    **Arguments:**
        * image: :class:`ImageField <django.db.models.ImageField>`
    """
    #image = models.ImageField(upload_to='photos/%Y/%m/%d')
    file = ImageWithThumbsField(upload_to='photos/%Y/%m/%d', sizes=((125, 125), (200,200)))
    
    class Meta:
        verbose_name_plural = 'Images'
        unique_together = (('slug', 'object_id', 'space', 'content_type'))
    
    def __unicode__(self):
        return "Image object (%s, %s)" % (self.title, self.file)
    
    # cant be used with ImageWithThumbField
    def set_location(self, location):
        file = self.file.__dict__.get('instance').__dict__.get('file')
        file.field.upload_to = location
        
        
class Root(models.Model):
    """
    Where all begins. The root directory.
    
    **Arguments:**
        title: CharField
        slug: SlugField
        space: :class:`Space <space.models.Space>`
        folders = GenericRelation(:class:`Folder <fhy.models.Folder>`)
        images = GenericRelation(:class:`ImageFHY <fhy.models.ImageFHY>`)
        files = GenericRelation(:class:`FileFHY <fhy.models.FileFHY>`)
    """
    #There's no need to add an author field, since the space is the object, represented
    #in the DB as an integer, so there's no possible way to select a non-wanted object.
    
    title = models.CharField(max_length=20, default='Personal Space')
    slug = models.SlugField()
    space = models.ForeignKey(Space, unique=True)
    folders = generic.GenericRelation(Folder)
    images = generic.GenericRelation(ImageFHY)
    files = generic.GenericRelation(FileFHY)
    # GenericRelation used for retrieving through a reverse relation with Folder.
    # You'll be able to do: r.folders.get/filter
    # Otherwise, it's impossible to access a ContentType ForeignKey
    
    class Meta:
        unique_together = (('slug', 'space'))
    
    def __unicode__(self):
        return "Root object (%s, %s)" % (self.slug, self.space)
    
#    def get_user_slug(self):
#        return self.space.user
         