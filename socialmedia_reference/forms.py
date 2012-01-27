from django.forms.models import ModelForm
from socialmedia_reference.models import SocialMediaReference

class SocialMediaForm(ModelForm):
    class Meta:
        model = SocialMediaReference
        exclude = ['user']