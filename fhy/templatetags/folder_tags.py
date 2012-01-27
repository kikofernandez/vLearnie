from django.db.models import get_model
from django import template
from fhy.models import Folder, Root
# {% get_folder_list idfolder as folder_list %}
def do_folder_list(parser, token):
    bits = token.split_contents()
    
    if len(bits) != 4:
        raise template.TemplateSyntaxError("get_folder_list takes exactly 3 arguments.")
    return ContentFolderList(bits[1], bits[3])

class ContentFolderList(template.Node):
    def __init__(self, idfolder, var_name):
        self.varname = var_name
        self.idfolder = template.Variable(idfolder)
        self.folder_list = []
    
    def render(self, context):
        idfolder = self.idfolder.resolve(context)
        current_folder = Folder.objects.get(id=idfolder)
        self.folder_list = [current_folder,]
        while(current_folder.content_type.name!='root'):
            current_folder = current_folder.content_object
            self.folder_list.append(current_folder)
        self.folder_list.append(current_folder.content_object)
        self.folder_list.reverse()
        
        context[self.varname] = self.folder_list
        return ''



def do_latest_files(parser, token):
    """
    Retrieves a list of filefhy/imagefhy given the model

    Example usage::

        {% get_latest_files fhy.filefhy space.slug 5 as latest_files %}
        {% get_latest_files fhy.imagefhy space.slug 5 as latest_images %}
        {% get_latest_files both space.slug 5 as latest_images_files %}
    """
    bits = token.split_contents()
    if len(bits) != 6:
        raise template.TemplateSyntaxError("'get_latest_content' tag takes exactly seven arguments")
    model2 = None
    if bits[1]=='both':
        model_args2 = 'fhy.filefhy'.split('.')
        model2 = get_model(*model_args2)
        model_args = 'fhy.imagefhy'.split('.')
    else:
        model_args = bits[1].split('.')
        model2 = None
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("First argument to 'get_latest_files' must be an 'application name'.'model name' string")
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError("'get_latest_files' tag got an invalid model: %s" % bits[1])
    return LatestContentNode(model, model2, bits[2], bits[3], bits[5])

class LatestContentNode(template.Node):
    def __init__(self, model, model2, spacename, num, varname):
        self.model = model
        self.model2 = model2 # models == (None or filefhy) always
        self.num = int(num)
        self.varname = varname
        self.spacename = template.Variable(spacename)
    
    def render(self, context):
        spacename = self.spacename.resolve(context)
        my_queryset = self.model._default_manager.filter(space__id = spacename).order_by('-pub_date')[:self.num]
        
        # We append the list to an empty list, and extend the list.
        # After that, we use a lambda function to order the list
        ordered_list = list()
        ordered_list.extend(my_queryset)
        if self.model2 is not None:
            my_queryset2 = self.model2._default_manager.filter(space__id = spacename).order_by('-pub_date')[:self.num]
            ordered_list.extend(my_queryset2)
        ordered_list.sort(key = lambda e: (e.pub_date, e.title))
        ordered_list.reverse()

        context[self.varname] = ordered_list[:5]
        return ''

register = template.Library()
register.tag('get_folder_list', do_folder_list)
register.tag('get_latest_files', do_latest_files)