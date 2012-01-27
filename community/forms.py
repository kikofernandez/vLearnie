from django.forms import ModelForm, HiddenInput, SlugField
from community.models import Community, Resource#EntryCommunityResource, URLCommunityResource

class CommunityForm(ModelForm):
    slug = SlugField(widget=HiddenInput)
    
    class Meta:
        model = Community
        #exclude = ['slug']

class ResourceForm(ModelForm):
    slug = SlugField(widget=HiddenInput)
    
    class Meta:
        model = Resource
        exclude = ['author', 'community']

#class EntryForm(ModelForm):
#    slug = SlugField(widget=HiddenInput)
#    
#    class Meta:
#        model = EntryCommunityResource
#        exclude = ['author', 'url_referrer']
        
#class URLForm(ModelForm):
#    slug = SlugField(widget=HiddenInput)
#    
#    class Meta:
#        model = URLCommunityResource
#        exclude = ['author', 'url_referrer']
