from django import template
from django.db.models import get_model
from coltrane.models import Entry, Link
from fhy.models import FileFHY
from tagging.models import Tag
#from tagging.utils import LINEAR, LOGARITHMIC

def do_latest_content(parser, token):
    """
    Retrieves a list of entries/links/filefhy given the model

    Example usage::

        {% get_latest_content coltrane.entry user.username space.slug 5 as latest_entries %}
    """
    bits = token.split_contents()
    if len(bits) != 7:
        raise template.TemplateSyntaxError("'get_latest_content' tag takes exactly seven arguments")
    model_args = bits[1].split('.')
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("First argument to 'get_latest_content' must be an 'application name'.'model name' string")
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError("'get_latest_content' tag got an invalid model: %s" % bits[1])
    return LatestContentNode(model, bits[2], bits[3], bits[4], bits[6])

class LatestContentNode(template.Node):
    def __init__(self, model, username, spacename, num, varname):
        self.model = model
        self.num = int(num)
        self.varname = varname
        self.username = template.Variable(username)
        self.spacename = template.Variable(spacename)
    
    def render(self, context):
        username = self.username.resolve(context)
        spacename = self.spacename.resolve(context)
        
        # If the model is Entry get the entries. The action is the same for all the models
        # but due to different attributes names, we must specified exactly which model
        # we want to consult.
        if Entry == self.model:
            if str(spacename).isdigit():
                my_queryset = self.model._default_manager.select_related().filter(author__username=username,
                                                                                  space__id=spacename)[:self.num]
            else:
                my_queryset = self.model._default_manager.select_related().filter(author__username=username,
                                                                                  space__slug=spacename)[:self.num]
        elif Link == self.model:
            if str(spacename).isdigit():
                my_queryset = self.model._default_manager.select_related().filter(posted_by__username = username,
                                                                                  space__id=spacename)[:self.num]
            else:
                my_queryset = self.model._default_manager.select_related().filter(posted_by__username = username,
                                                                                  space__slug=spacename)[:self.num]
        elif FileFHY == self.model:
            my_queryset = self.model._default_manager.select_related().filter(space__id = spacename)[:self.num]
        context[self.varname] = my_queryset
        return ''


def do_tags_cloud_for_model(parser, token):
    """
    Retrieves a tag cloud for the given model

    Example usage::

        {% tags_cloud_for_model articles.Article username spacename as object_list %}
        {% tags_cloud_for_model articles.Article username spacename as object_list step 6 %}
    """
    step = 4
    bits = token.contents.split()
    if len(bits) < 6:
        raise template.TemplateSyntaxError('%s tag requires six arguments' % bits[0])
    if bits[4] != 'as':
        raise template.TemplateSyntaxError("fourth argument to %s tag must be 'as'"% bits[0])
    if len(bits) > 4:
        if bits[6] != 'step':
            raise template.TemplateSyntaxError("optional sixth argument to %s tag must be 'step'" % bits[0])
        try:
            step = int(bits[7])
        except IndexError:
            raise template.TemplateSyntaxError("optional seventh argument after step is required")
        except ValueError:
            raise template.TemplateSyntaxError("optional seventh argument after step is not an integer")
    return TagsCloudForModelNode(bits[1], bits[2], bits[3], bits[5], step)


class TagsCloudForModelNode(template.Node):
    def __init__(self, model, username, spacename ,varname, step):
        self.varname, self.step = varname, step
        self.username, self.spacename = template.Variable(username), template.Variable(spacename)
        self.model = get_model(*model.split('.'))

    def render(self, context):
        username = self.username.resolve(context)
        spacename = self.spacename.resolve(context)
        # filters is used to filter the model via a lookup by the values in the filter dict
        filters = {'author__username': username, 'space__slug': spacename}
        context[self.varname] = Tag.objects.cloud_for_model(self.model,
                                                            self.step,
                                                            filters= filters)
        return ''

    
# Register the library of template tags
register = template.Library()

register.tag('get_latest_content', do_latest_content)
register.tag('tags_cloud_for_model', do_tags_cloud_for_model)