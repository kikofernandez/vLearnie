from piston.handler import BaseHandler, AnonymousBaseHandler
#from coltrane.models import *
from community.models import Community, Resource
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.defaultfilters import slugify
from piston.utils import throttle


class AnonymousCommunitytHandler(AnonymousBaseHandler):
    allowed_methods = ('GET', )
    model = Community
    fields = ('id', 'title', 'excerpt')
    
    @throttle(5, 60*10)
    def read(self, request, id=None):
        base = Community.objects
        
        if id:
            return base.get(id=id)
        else:
            return base.all()

class AnonymousResourceHandler(AnonymousBaseHandler):
    allowed_methods = ("GET",)
    model = Resource
    fields = ('id','community', 'title', 'author', 'pub_date', 'excerpt', 'body_html',)
    
    @throttle(5, 60*10)
    def read(self, request, id=None, resource_id=None):
        community = Community.objects
        resource = Resource.objects
        
        if id is not None:
            if resource_id is None:
                return community.get(pk=id).resource_set.filter(type=0)
            else:
                return resource.get(pk=resource_id)
        else:
            return False

class CommunityHandler(BaseHandler):
    allowed_methods = ('GET','POST', 'PUT', 'DELETE')
    model = Community
    anonymous = AnonymousCommunitytHandler
    fields = ('id', 'title', 'excerpt', 'description')
    
    def read(self, request, id=None):
        community = Community.objects
        if id is None:
            return community.all()
        else:
            return community.get(pk=id)
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            title = attrs['title']
            slug = slugify(title)
        except KeyError:
            return "You must write the mandatory arguments"
        
        excerpt = attrs['excerpt']
        description = attrs['description']
        comm = Community(title=title, slug=slug,
                         excerpt=excerpt,
                         description=description)
        comm.save()
        return comm
    
    def update(self, request, id):
        if request.user.is_superuser:
            try:
                comm = Community.objects.get(pk=id)
            except Community.DoesNotExist:
                return "The community object does not exist"
            attrs = self.flatten_dict(request.PUT)
            title = attrs.get('title')
            if title is not None:
                comm.title = title
                comm.slug = slugify(title)
            
            excerpt = attrs.get('excerpt')
            if excerpt is not None:
                comm.excerpt = excerpt
            
            description = attrs.get('description')
            if description is not None:
                comm.description = description
            
            comm.save()
            return comm
        return "Operation only allowed for the administrator"

    def delete(self, request, id):
        if request.user.is_superuser:
            try:
                comm = Community.objects.get(pk=id)
            except Community.DoesNotExist:
                return "The community object does not exist"
            comm.delete()
            return ""
        return "Operation only allowed for the administrator"

class ResourceHandler(BaseHandler):
    allowed_methods = ("GET", "POST",)
    model = Resource
    anonymous = AnonymousResourceHandler
    fields = ('id',('community', ('title',)), 'title', ('author', ('username',)),
              'pub_date', 'excerpt', 'body_html', 'tags')
    
    def read(self, request, id=None, resource_id=None):
        community = Community.objects
        resource = Resource.objects
        
        if id is not None:
            if resource_id is None:
                return community.get(pk=id).resource_set.filter(type=0)
            else:
                return resource.get(pk=resource_id)
        else:
            return False

class DefaultResourceHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Resource
    fields = ('id',('community', ('title',)), 'title', ('author', ('username',)),
              'pub_date', 'excerpt', 'body', 'tags')
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            community = Community.objects.get(pk=attrs['community'])
            title = attrs['title']
            author = request.user
            slug = slugify(title)
            pub_date = attrs['pub_date']
            type = attrs['type']
            if int(type) not in range(1, 4):
                raise "Bad type specified"
        except KeyError:
            return "There is at least one mandatory object not initialised"
        except Community.DoesNotExist:
            return "The Community object does not exist"
        excerpt = attrs.get('excerpt')
        
        tags = attrs.get('tags')
        body = attrs.get('body')
        resource = Resource(community=community,
                            title=title,
                            slug=slug,
                            pub_date=pub_date,
                            type=type,
                            excerpt=excerpt,
                            tags=tags,
                            body=body,
                            author=author)
        resource.save()
        return resource
        
    
    def update(self, request, id):
        try:
            resource = Resource.objects.get(pk=id)
        except Resource.DoesNotExist:
            return "The resource does not exist"
        if resource.author == request.user:
            attrs = self.flatten_dict(request.PUT)
            title = attrs.get('title')
            if title is not None:
                resource.title = title
                resource.slug = slugify(title)
            
            pub_date = attrs.get('pub_date')
            if pub_date is not None:
                resource.pub_date = pub_date
            
            type = attrs.get('type')
            if type is not None:
                resource.type = type
            
            excerpt = attrs.get('excerpt')
            if excerpt is not None:
                resource.excerpt = excerpt
            
            tags = attrs.get('tags')
            if tags is not None:
                resource.tags = tags
            
            body = attrs.get('body')
            if body is not None:
                resource.body = body
            
            resource.save()
            return resource
        return "You are not the author of this resource."
    
    def delete(self, request, id):
        try:
            resource = Resource.objects.get(pk=id)
        except Resource.DoesNotExist:
            return "Resource does not exist"
        if resource.author == request.user:
            resource.delete()
            return ""
        return "You are not allowed to do this operation"