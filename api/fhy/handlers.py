'''
Created on 16/05/2011

@author: kikofernandezreyes
'''
from piston.handler import BaseHandler
from piston.utils import rc
from fhy.models import Root, Folder, FileFHY, ImageFHY
from django.contrib.contenttypes.models import ContentType
from space.models import Space
from django.template.defaultfilters import slugify
import datetime
from django.core.files.uploadedfile import UploadedFile


CONTENT_TYPE = ['root', 'folder']

class FHYRootHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = ('id', 'slug','title', 'pub_date','file', 'description')
    
    def read(self, request, space_id):
        root = Root.objects.get(space__id=space_id,
                                space__user__username = request.user.username)
        return root.files.all(), root.images.all(), root.folders.all()

class FHYFolderHandler(BaseHandler):
    allowed_methods = ('GET')
    
    def read(self, request, space_id, folder_id):
        folder = Folder.objects.get(id=folder_id)
        filefhy = FileFHY.objects.filter(content_type__name=u'folder',
                                         object_id=folder.id)
        imagefhy = ImageFHY.objects.filter(content_type__name=u'folder',
                                           object_id=folder.id)
        folder = ImageFHY.objects.filter(content_type__name=u'folder',
                                         object_id=folder.id)
        return filefhy, imagefhy, folder

class AnonymousFHYFileHandler(BaseHandler):
    allowed_methods = ("GET",)
    fields = ('title', 'space_id', 'id', 'file', 'pub_date',
              'description')
    
    def read(self, request, username):
        return FileFHY.objects.filter(space__user__username=username)

class FHYFileHandler(BaseHandler):
    allowed_methods = ("GET",)
    anonymous = AnonymousFHYFileHandler
    fields = ('title', 'space_id', 'id', 'file', 'pub_date',
              'description')
    
    def read(self, request, username):
        return FileFHY.objects.filter(space__user__username=username)

class AnonymousFHYImageHandler(BaseHandler):
    allowed_methods = ("GET",)
    fields = ('title', 'space_id', 'id', 'file', 'pub_date',
              'description')
    
    def read(self, request, username):
        return ImageFHY.objects.filter(space__user__username=username)

class FHYImageHandler(BaseHandler):
    allowed_methods = ("GET",)
    anonymous = AnonymousFHYImageHandler
    fields = ('title', 'space_id', 'id', 'file', 'pub_date',
              'description')
    
    def read(self, request, username):
        return ImageFHY.objects.filter(space__user__username=username)
        
class FHYFileRemoverHandler(BaseHandler):
    allowed_methods = ('DELETE',)
    
    def delete(self, request, id):
        file = FileFHY.objects.get(pk=id)

        if not request.user.id == file.space.user_id:
            return rc.FORBIDDEN
        
        file.delete()
        
        return rc.DELETED

class FHYImageRemoverHandler(BaseHandler):
    allowed_methods = ('DELETE',)
    
    def delete(self, request, id):
        file = ImageFHY.objects.get(pk=id)
        
        if not request.user.id == file.space.user_id:
            return rc.FORBIDDEN
        
        file.delete()
        
        return rc.DELETED

def handle_uploaded_file(f):
    """
    This function will upload a file
    """
    destination = open(f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

class DefaultFileHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = FileFHY
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            title = attrs['title']
            slug = slugify(title)
            space = Space.objects.get(pk=attrs['space'])
            object_id = Root.objects.get(space=space,
                                         space__user=request.user)
#            if attrs['content_type'] in CONTENT_TYPE:
            content_type = ContentType.objects.select_related(depth=2).get(name='root')
#            else:
#                raise ContentType.DoesNotExist
            
#            content_object = generic.GenericForeignKey()
        except (KeyError, ContentType.DoesNotExist):
            return "There are mandatory fields that were not specified"
        except (Space.DoesNotExist, Root.DoesNotExist):
            return "The space id or the Root does not exist"
        description = "" if attrs.get('description') is None else attrs['description']
        pub_date = datetime.date.today().strftime('%Y-%m-%d')
        
        file_uploaded = request.FILES['file']
        handle_uploaded_file(file_uploaded)
        
        file = FileFHY(title=title, slug=slug, space=space, object_id=object_id.id,
                       content_type=content_type, description=description, 
                       pub_date=pub_date,
                       file=file_uploaded)
        file.save()
        return rc.ALL_OK
    
    def update(self, request, id):
        attrs = self.flatten_dict(request.POST)
        try:
#            if attrs['file_type']=='file':
            file = FileFHY.objects.get(pk=id)
#            else:
#                file = ImageFHY.objects.get(pk=id)
        except (FileFHY.DoesNotExist, ImageFHY.DoesNotExist):
            return rc.NOT_FOUND
        
        if file.space.user != request.user:
            return rc.FORBIDDEN
        
        title = attrs.get('title')
        if title is not None:
            file.title = title
            file.slug = slugify(title)
            
        description = attrs.get('description')
        if description is not None:
            file.description = description
             
        pub_date = datetime.date.today().strftime('%Y-%m-%d')
        file.pub_date = pub_date
        
        if request.FILES['files'] is not None:
            file_uploaded = request.FILES['file']
            handle_uploaded_file(file_uploaded)
            file.file = file_uploaded
        
        file.save()
        return rc.ALL_OK
    
    def delete(self, request, id):
        try:
            file = FileFHY.objects.get(pk=id)
        except FileFHY.DoesNotExist:
            return rc.NOT_FOUND
        if file.space.user == request.user:
            file.detele()
            return rc.DELETED
        else:
            return rc.FORBIDDEN

class DefaultImageHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = ImageFHY
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            title = attrs['title']
            slug = slugify(title)
            space = Space.objects.get(pk=attrs['space'])
            object_id = Root.objects.get(space=space,
                                         space__user=request.user)
#            if attrs['content_type'] in CONTENT_TYPE:
            content_type = ContentType.objects.select_related(depth=2).get(name='root')
#            else:
#                raise ContentType.DoesNotExist
            
#            content_object = generic.GenericForeignKey()
        except (KeyError, ContentType.DoesNotExist):
            return "There are mandatory fields that were not specified"
        except (Space.DoesNotExist, Root.DoesNotExist):
            return "The space id or the Root does not exist"
        description = "" if attrs.get('description') is None else attrs['description']
        pub_date = datetime.date.today().strftime('%Y-%m-%d')
        
        file_uploaded = request.FILES['file']
        handle_uploaded_file(file_uploaded)
        
        file = ImageFHY(title=title, slug=slug, space=space, object_id=object_id.id,
                       content_type=content_type, description=description, 
                       pub_date=pub_date,
                       file=file_uploaded)
        file.save()
        return rc.ALL_OK
    
    def update(self, request, id):
        attrs = self.flatten_dict(request.POST)
        try:
#            if attrs['file_type']=='file':
            file = ImageFHY.objects.get(pk=id)
#            else:
#                file = ImageFHY.objects.get(pk=id)
        except (FileFHY.DoesNotExist, ImageFHY.DoesNotExist):
            return rc.NOT_FOUND
        
        if file.space.user != request.user:
            return rc.FORBIDDEN
        
        title = attrs.get('title')
        if title is not None:
            file.title = title
            file.slug = slugify(title)
            
        description = attrs.get('description')
        if description is not None:
            file.description = description
             
        pub_date = datetime.date.today().strftime('%Y-%m-%d')
        file.pub_date = pub_date
        
        if request.FILES['files'] is not None:
            file_uploaded = request.FILES['file']
            handle_uploaded_file(file_uploaded)
            file.file = file_uploaded
        
        file.save()
        return rc.ALL_OK
    
    def delete(self, request, id):
        try:
            file = ImageFHY.objects.get(pk=id)
        except ImageFHY.DoesNotExist:
            return rc.NOT_FOUND
        if file.space.user == request.user:
            file.detele()
            return rc.DELETED
        else:
            return rc.FORBIDDEN