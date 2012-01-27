from django.forms import ModelForm
from friendycontrol.models import FriendPerson, FriendListGroupName, Readable,CompositionList
from django.forms.models import ValidationError

from space.models import Space

class FriendPersonForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(FriendPersonForm, self).__init__(*args, **kwargs)
        
        if self.instance:
            group_name_query = FriendListGroupName.objects.filter(owner=user)
            self.fields['group_list'].queryset = group_name_query
        # = ModelMultipleChoiceField(queryset=group_name_query)
    class Meta:
        model = FriendPerson
        exclude = ['friend_of']
    
    def clean_group_list(self):
        data = self.cleaned_data['group_list']
        for data_object in data:
            valid = FriendListGroupName.objects.filter(id=data_object.id)
        #valid = FriendListGroupName.objects.get(id=data)
        
        if not valid:
            raise ValidationError('Please, select a group list that belongs to you')
        return data

class FriendListForm(ModelForm):

    class Meta:
        model = FriendListGroupName
        exclude = ['owner', 'slug']

class ReadableForm(ModelForm):
    class Meta:
        model = Readable
        exclude = ['foreign_group']
        
class CompositionListForm(ModelForm):
    def __init__(self, owner, *args, **kwargs):
        super(CompositionListForm, self).__init__(*args, **kwargs)
        
        if self.instance:
            owner_queryset = FriendListGroupName.objects.filter(owner=owner)
            space_queryset = Space.objects.filter(user=owner)
            self.fields['composition_list'].queryset = owner_queryset
            self.fields['spaces'].queryset = space_queryset
    
    class Meta:
        model = CompositionList
        exclude = ['owner']
        

#class AppForm(Form):
#    perm_space = ModelMultipleChoiceField(queryset=None)
#    
#    def __init__(self, user, initial=None, *args, **kwargs):
#        super(AppForm, self).__init__(*args, **kwargs)
#        
#        space_queryset = Space.objects.filter(user=user)
#        self.fields['perm_space'].queryset = space_queryset
#        if initial:
#            self.initial = initial 