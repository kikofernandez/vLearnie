from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc
#from coltrane.models import *
from coltrane.models import Entry
from space.models import Space
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.defaultfilters import slugify


class AnonymousBlogPostHandler(AnonymousBaseHandler):
    allowed_methods = ('GET', )
    model = Entry
    fields = (('author', ('username', 'first_name', 'last_name', 'id')),
              ('space', ('title','id')),'title','body',
              ('pub_date'),
             )
    
    def read(self, request, author=None, space=None, pub_date=None):
        base = Entry.objects
        if author and space and pub_date:
            return base.filter(author__username=author,
                               space=space,
                               pub_date = pub_date)
        elif author and space:
            return base.filter(author__username=author,
                               space=space)
        elif author:
            return base.filter(author__username=author)[:10]
        else:
            raise Http404("No se ha introducido un autor")

class BlogPostHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Entry
    anonymous = AnonymousBlogPostHandler
    fields = (('author', ('username', 'first_name', 'last_name', 'id')),
              ('space', ('title','id')),'title',
              ('pub_date'),
              'body', 'id'
             )
    
    def read(self, request, author=None, space=None, pub_date=None):
        base = Entry.objects
        if author and space and pub_date:
            return base.filter(author__username=author,
                               space=space,
                               pub_date = pub_date)
        elif author and space:
            return base.filter(author__username=author,
                               space=space)
        elif author:
            return base.filter(author__username=author)[:10]
        else:
            raise Http404("No se ha introducido un autor")

class DefaultBlogPostHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Entry
    fields = (('author', ('username', 'first_name', 'last_name', 'id')),
              ('space', ('title','id')),'title',
              ('pub_date'),
              'body', 'id'
             )
    
    def read(self, request, id=None):
        base = Entry.objects
        if id is None:
            return base.filter(author=request.user)
        else:
            try:
                entry =  base.get(author=request.user,
                                  pk=id)
                return entry
            except Entry.DoesNotExist:
                return rc.NOT_FOUND
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        space_obj = get_object_or_404(Space, pk=attrs['spaceid'])
        try:
            slug = slugify(attrs['title'])
            tags = attrs.get('tags')
            # The status is a numeric value, see models
            status = Entry.LIVE_STATUS if attrs.get('status') is None else attrs.get('status')
            
            pub_date = attrs.get('pub_date')
            entry = Entry(body=attrs['body'],
                     author=request.user,
                     space=space_obj,
                     title=attrs['title'],
                     slug=slug,
                     tags=tags,
                     status=status,
                     pub_date=pub_date)
        except Exception:
            return "An exception ocurred. This may be due to an ilegal value," \
                    "or mandatory value not initialized"
        entry.save()
        return entry
    
    def update(self, request, id):
        entry = get_object_or_404(Entry, pk=id)
        if entry.author == request.user:
            attrs = self.flatten_dict(request.PUT)
            if attrs.get('spaceid') is not None:
                space_obj = Space.objects.get(pk=attrs['spaceid'])
                entry.space = space_obj 
            
            if attrs.get('title') is not None:
                entry.title = attrs.get('title')
                slug = slugify(attrs['title'])
                entry.slug = slug
            
            if attrs.get('body') is not None:
                entry.body = attrs.get('body') 
            
            if attrs.get('tags') is not None:
                entry.tags = attrs['tags']
            
            if attrs.get('status') is not None:
                if attrs['status'] in range(1, 4):
                    entry.status = attrs['status']
                else:
                    return "Error, the status was not correct."
                
            if attrs.get('pub_date') is not None:
                entry.pub_date = attrs['pub_date']
            
            entry.save()
            return entry
        return "Error, you cannot change an entry if you are not the author"
    
    def delete(self, request, id):
        entry = Entry.objects.get(pk=id)
        if entry.author == request.user:
            entry.delete()
            return ""
        return "You are not allowed to delete someone else's entry"
