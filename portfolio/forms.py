from django import forms
from django.forms.extras.widgets import SelectDateWidget
from portfolio import models
from django.forms.models import ModelForm
import datetime

# constants
MIN_YEAR = 1950
MAX_YEAR = datetime.date.today().year+1

class ProjectForm(forms.ModelForm):
    #def __init__(self, category=None, *args, **kwargs):
    def __init__(self, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
#        if category is not None:
        if user is not None:
#            choices = ((cat.id, cat.name) for cat in category)
            choices = ((cat.id, cat.name) for cat in models.Category.objects.filter(user=user))
            self.fields['category'].choices = choices
            #self.fields['category'] = forms.ChoiceField(choices=choices)
            
            choices = ((cat.id, cat.name) for cat in models.Skill.objects.filter(user=user))
            #self.fields['skills'].queryset = choices
            self.fields['skills'] = forms.MultipleChoiceField(choices=choices)
    
    slug = forms.SlugField(widget=forms.HiddenInput)
    
    class Meta:
        model = models.Project
        exclude = ['user', 'space']
        
class SkillForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.HiddenInput)
    
    class Meta:
        model = models.Skill
        exclude = ['user']
        
class CategoryForm(ModelForm):
    slug = forms.SlugField(widget=forms.HiddenInput)
    
    class Meta:
        model = models.Category
        exclude = ['user', 'position']

class PersonalInformationForm(ModelForm):
    birthday = forms.DateField(widget=SelectDateWidget(
                        years=[x for x in range(MIN_YEAR, int(datetime.date.today().year))])
    )
    
    class Meta:
        model = models.PersonalInformation
        exclude = ['user']
        
class StudyForm(ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'60'}))
    place = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'60'}))
    start  = forms.DateField(widget=SelectDateWidget(
                            years=[x for x in range(MIN_YEAR, MAX_YEAR)])
    )
    end  = forms.DateField(widget=SelectDateWidget(
                            years=[x for x in range(MIN_YEAR, MAX_YEAR)])
    )
    required_css_class = 'required'
    
    class Meta:
        model= models.Study
        exclude = ['user']