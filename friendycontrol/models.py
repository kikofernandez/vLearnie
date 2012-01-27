from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from space.models import Space

class FriendListGroupName(models.Model):
    """
    This is the list of friends (FriendList).
    
    **Arguments:**
        * id: AutoField
        * group_name: CharField
        * slug: SlugField
        * owner: :class:`User <django.contrib.auth.models.User>`
        * description: TextField
    """
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=40)
    slug = models.SlugField()
    owner = models.ForeignKey(User)
    description = models.TextField(blank=True,
                                   help_text = "Optional.")
    
    class Meta:
        # unique_together, so that the user cannot create two list with the same name
        # slug is a hidden field
        unique_together = (('slug', 'owner'))
    
    def __unicode__(self):
        return self.group_name

class CompositionList(models.Model):
    """
    CompositionList allows the user the composition of a list of friends, 
    joining different FriendLists
    
    **Arguments:**
        * id: AutoField
        * composition_list: ManyToManyField(:class:`FriendListGroupName <friendycontrol.models.FriendListGroupName>`)
        * owner = :class:`User <django.contrib.auth.models.User>`
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    composition_list = models.ManyToManyField(FriendListGroupName)
    owner = models.ForeignKey(User)
    spaces = models.ManyToManyField(Space)
    
    def __unicode__(self):
        return self.name
    

class FriendPerson(models.Model):
    """
    FriendPerson, object that joins friend Users inside the FriendListGroupName.
    
    **Arguments:**
        * id: AutoField
        * friend: :class:`User <django.contrib.auth.models.User>`
        * friend_of: :class:`User <django.contrib.auth.models.User>`
        * group_list: ManyToManyField(:class:`FriendListGroupName <friendycontrol.models.FriendListGroupName>`)
    """
    id = models.AutoField(primary_key=True)
    friend = models.ForeignKey(User, related_name='friend_set')
    friend_of = models.ForeignKey(User, related_name='friendof_set')
    group_list = models.ManyToManyField(FriendListGroupName, blank=True)
    
    class Meta:
        unique_together = (('friend_of', 'friend'))
    
    def __unicode__(self):
        return "%s, %s %s" % (self.friend.username, self.friend.first_name, self.friend.last_name)

class Readable(models.Model):
    """
    Readable is an object that will point to the FriendListGroupName object. Readable
    is the object that will grant read permissions to the users that are related with
    the FriendListGroupName object.
    
    **Arguments:**
        * id: AutoField
        * read: BooleanField, default= **False**
        * foreign_group: :class:`CompositionList <friendycontrol.models.CompositionList>`
    """
    id = models.AutoField(primary_key=True)
    read = models.BooleanField(default=False)
    foreign_group = models.ForeignKey(CompositionList, unique=True)
    
    def __unicode__(self):
        return "Readable: (%s, %s)" % (self.id, self.read)

class RelationModel(models.Model):
    """
    RelationalModel is a model that joins objects from any model with a Readable object.
    
    **Arguments:**
        * id: AutoField
        * readable: :class:`Readable <friendycontrol.models.Readable>`
        * content_type: ContentType
        * content_object: GenericForeignKey()
    """
    id = models.AutoField(primary_key=True)
    readable = models.ForeignKey(Readable)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()
    
    def __unicode__(self):
        return "RelationalModel: (%s, %s)" % (self.id, self.content_type)
    