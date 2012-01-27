from django.forms import ModelForm, HiddenInput, SlugField, \
                            IntegerField, Form, ModelMultipleChoiceField, ValidationError
from fhy.models import Folder, ImageFHY, FileFHY, MAX_FILE_SIZE
from community.models import Community
from django.forms import FileField
from django.contrib.admin.widgets import AdminFileWidget
from djangothumbs.thumbs import ImageWithThumbsField

class FolderForm(ModelForm):
    slug = SlugField(widget=HiddenInput)
    
    class Meta:
        model = Folder
        exclude = ['id','space', 'object_id', 'content_type']

class ResourceForm(ModelForm):
    slug = SlugField(widget=HiddenInput)
    

class ImageFHYForm(ResourceForm):    
    file = ImageWithThumbsField(upload_to='photos/%Y/%m/%d', sizes=((125, 125), (200,200)))
    
    class Meta:
        model = ImageFHY
        exclude = ['space', 'object_id', 'content_type', 'pub_date']
        
class FileFHYForm(ResourceForm):
    file = FileField(widget=AdminFileWidget(), required=False)
    
    def clean_file(self):
        if self.cleaned_data['file'].size > MAX_FILE_SIZE:
            raise ValidationError('Filesize bigger than %s Kb' % str(MAX_FILE_SIZE)[:-3])
        return self.cleaned_data['file']
        
    class Meta:
        model = FileFHY
        exclude = ['space', 'object_id', 'content_type', 'pub_date']
        
class CommunityFileForm(Form):
    type = IntegerField(widget=HiddenInput)
    community = ModelMultipleChoiceField(queryset=Community.objects.all())
    
    def __init__(self, instance=None, *args, **kwargs):
        super(CommunityFileForm, self).__init__(*args, **kwargs)

        if instance is not None:
            self.initial = instance
    