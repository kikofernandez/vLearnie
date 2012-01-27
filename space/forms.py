from django.forms import ModelForm, SlugField, HiddenInput,Textarea, ModelMultipleChoiceField, CharField
from coltrane.models import Entry, Category, Link
from space.models import Space
from django.http import Http404
from community.models import Community

class EntryForm(ModelForm):
    #def __init__(self, categoryset=None, communityset=None, *args, **kwargs):
    def __init__(self, categoryset=None, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        communityset = Community.objects.select_related(depth=2)
        if categoryset is not None and communityset is not None:
            self.fields['categories'] = ModelMultipleChoiceField(queryset=categoryset)
        
    slug = SlugField(widget=HiddenInput)

    
    class Meta:
        model = Entry
        exclude = ['space', 'author']

class CategoryForm(ModelForm):
    slug = SlugField(widget=HiddenInput)
    #space = SlugField(widget=HiddenInput)
    description = Textarea()
    
    class Meta:
        model = Category
        exclude = ['space', 'author']
        

class SpaceForm(ModelForm):
    slug = SlugField(widget=HiddenInput)
    
    class Meta:
        model = Space
        exclude = ['user']
    
#    def validate_unique(self):
#        try:
#            self.instance.validate_unique()
#        except IntegrityError:
#            self._update_errors({'IntegrityError': 'Error de integridad'})

class LinkForm(ModelForm):
    slug = SlugField(widget=HiddenInput)
    
    class Meta:
        model = Link
        exclude = ['space', 'posted_by']