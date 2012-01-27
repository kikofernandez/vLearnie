from django import template
from socialmedia_reference.models import SocialMediaReference

def do_socialmedia_list(parser, token):
    """
    {% get_socialmedia user.username as socialmedia %}
    """
    bits = token.split_contents()
    
    if len(bits) != 4:
        raise template.TemplateSyntaxError("get_socialmedia takes exactly 3 arguments.")
    return SocialMediaList(bits[1], bits[3])

class SocialMediaList(template.Node):
    def __init__(self, username, varname):
        self.varname = varname
        self.username = template.Variable(username)
        self.socialmedia_list = []
    
    def render(self, context):
        username = self.username.resolve(context)
        self.socialmedia_list = SocialMediaReference.objects.filter(user__username=username)
        context[self.varname] = self.socialmedia_list
        return ''

register = template.Library()
register.tag('get_socialmedia', do_socialmedia_list)