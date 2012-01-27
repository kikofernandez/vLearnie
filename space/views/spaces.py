from space.models import Space
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.admin.models import User
from django.contrib.auth import decorators
from django.forms import ModelForm, SlugField, HiddenInput, DateField
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from space.exceptions import DuplicateValuesAreNotUnique
from coltrane.models import Entry
from space.forms import EntryForm, SpaceForm
#from django.core.context_processors import csrf
from django.template import RequestContext
from portfolio.models import PersonalInformation
from django.http import Http404

def create_space(request):
    if request.method == 'POST':
        form = SpaceForm(data = request.POST)
        try:
            if form.is_valid():
                new_space = form.save(commit=False)
                #print new_space.slug
                new_space.user = request.user
                #new_space.slug = slugify(new_space.title)
                space_exist = Space.objects.filter(user=new_space.user).filter(title=new_space.title)
                if space_exist:
                    raise DuplicateValuesAreNotUnique
                new_space.save()
                return HttpResponseRedirect(reverse('space_space_list_spaces'))
        except DuplicateValuesAreNotUnique:
            form.non_field_errors = "The title of this space already exist. Please choose another one."
    else:
        form = SpaceForm()
    return render_to_response('space/space_form.html',
                              {'form': form,
                               'add':True},
                              context_instance=RequestContext(request))
create_space = decorators.login_required(create_space)

def edit_space(request, id):
    space = get_object_or_404(Space, user=request.user, id=id)
    if request.method == 'POST':
        form = SpaceForm(instance=space, data = request.POST)
        try:
            if form.is_valid():
                new_space = form.save(commit=False)
                space_exist = Space.objects.filter(user=new_space.user,
                                                   title=new_space.title)
                if space_exist:
                    raise DuplicateValuesAreNotUnique
                new_space.save()
                return HttpResponseRedirect(reverse('space_space_list_spaces'))
        except DuplicateValuesAreNotUnique:
            form.non_field_errors = "The title of this space already exist. Please choose another one."
    else:
        form = SpaceForm(instance=space)
    return render_to_response('space/space_form.html',
                              {'form':form,
                               'add':False},
                               context_instance=RequestContext(request))
edit_space = decorators.login_required(edit_space)

def show_my_spaces(request):
    return object_list(request,
                       queryset=Space.objects.filter(user=request.user),
                       template_name="space/spaces_by_user.html",
                       extra_context={'user': request.user})
show_my_spaces = decorators.login_required(show_my_spaces)


def show_user_space(request, space_name):
    space = get_object_or_404(Space, slug = space_name,
                                     user = request.user)    
    try:
        bio = get_object_or_404(PersonalInformation, user=request.user)
    except Http404:
        bio = None
    blog = space.entry_set.all()[:5]
    return object_list(request,
                       queryset=blog, 
                       template_name='space/resume_space.html', 
                       extra_context = {'user': request.user,
                                        'space': space,
                                        'bio': bio},
                       )
show_user_space = decorators.login_required(show_user_space)