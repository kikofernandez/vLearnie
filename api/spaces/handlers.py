from piston.handler import BaseHandler
from piston.utils import rc
from django.template.defaultfilters import slugify
from space.models import Space

class SpaceHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')
    model = Space
    fields = ('id', 'title', 'slug',
              ('user', ('first_name', 'last_name', 'username')))
    
    def read(self, request, id=None):
        base = Space.objects
        
        if id is None:
            return base.filter(user=request.user)
        else:
            try:
                space = base.get(user=request.user,
                                   pk=id)
                return space
            except Space.DoesNotExist:
                return rc.NOT_FOUND
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            title = attrs['title']
            slug = slugify(title)
        except KeyError:
            return rc.BAD_REQUEST
        
        space = Space(title=title, slug=slug, user=request.user)
        space.save()
        return space
    
    def update(self, request, id):
        try:
            space = Space.objects.get(pk=id)
        except Space.DoesNotExist:
            return rc.NOT_FOUND
        
        attrs = self.flatten_dict(request.PUT)
        try:
            title = attrs['title']
            space.title = title
            
            slug = slugify(title)
            space.slug = slug
            space.save()
        except KeyError:
            return rc.BAD_REQUEST
        return space