from django.shortcuts import Http404, render_to_response, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import decorators
#from friendycontrol.models import *
from friendycontrol.models import FriendListGroupName, FriendPerson, \
                                    CompositionList, RelationModel, Readable
from friendycontrol.exceptions import DuplicateValuesAreNotUnique
from friendycontrol.forms import FriendPersonForm, FriendListForm, \
                                CompositionListForm, ReadableForm
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db import IntegrityError
from django.template.defaultfilters import slugify
from space.models import Space

def show_main_friendylist(request):
    """
    This function returns a list with the friend list belonging to the user.
    
    **Template:**
    ``friendycontrol/friendlist_content.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    friendlist = FriendListGroupName.objects.select_related(depth=2).filter(owner=request.user)
    return object_list(request, 
                       queryset= friendlist, 
                       template_name='friendycontrol/friendlist_content.html',
                       extra_context=None)
show_main_friendylist = decorators.login_required(show_main_friendylist)
#show_main_friendylist = show_if_permitted(show_main_friendylist)

def show_main_friends(request):
    """
    Shows a list of friends objects
    
    **Template:**
    ``friendycontrol/friends_content.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    friends = FriendPerson.objects.filter(friend_of=request.user)
    return object_list(request,
                       queryset=friends, 
                       template_name='friendycontrol/friends_content.html',
                       #extra_context,
                       )
show_main_friends = decorators.login_required(show_main_friends)

def show_main_compositions(request):
    """
    Shows a list of composition objects
    
    **Template:**
    ``friendycontrol/compositions_content.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    compositions = CompositionList.objects.filter(owner=request.user)
    return object_list(request,
                       queryset=compositions,
                       template_name='friendycontrol/compositions_content.html',
                       )
show_main_compositions = decorators.login_required(show_main_compositions)

def add_friend(request):
    """
    This function creates a new :class:`friendycontrol.FriendPerson` object. 
    If everything was right,
    after submiting the content you must be redirected to a page where the 
    friendlist is shown.
    
    **Template:**
    ``friendycontrol/friend_form.html``
    
    **Context:**
        ``form``: The form object to render.
        
        ``add``: ``True`` if you want to re-mark that is an *add* operation.
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    if request.method == 'POST':
        form = FriendPersonForm(request.user, data=request.POST)
        try:
            if form.is_valid():
                friendperson = form.save(commit=False)
                friendperson.friend_of = request.user
                try:
                    get_object_or_404(FriendPerson, friend=friendperson.friend,
                                                    friend_of = request.user)                
                except Http404:
                    friendperson.save()
                    form.save_m2m()
                    return HttpResponseRedirect(reverse('friendy_show_main_friends'))
                else:
                    raise DuplicateValuesAreNotUnique
        except DuplicateValuesAreNotUnique:
            form.non_field_errors = 'Already exists this friend.'
    else:
        form = FriendPersonForm(request.user)
    return render_to_response('friendycontrol/friend_form.html',
                              {'form': form,
                               'add': True},
                              context_instance = RequestContext(request))
add_friend = decorators.login_required(add_friend)

def edit_friend(request, id):
    """
    Use this function if you want to edit a friend list.
    It takes an ``id`` argument, which is the **friend id**
    
    **Template:**
    ``friendycontrol/friend_form.html``
    
    **Context:**
        ``form``: The form object to render
        
        ``add``: ``True`` if you want to re-mark that is an *add* operation
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    try:
        friend = get_object_or_404(FriendPerson, id=id,
                                                 friend_of=request.user)
    except Http404:
        raise Http404("This friend does not exist.")
    if request.method == 'POST':
        form = FriendPersonForm(request.user, instance=friend, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('friendy_show_main_friends'))
    else:
        form = FriendPersonForm(request.user, instance=friend)
    return render_to_response('friendycontrol/friend_form.html',
                              {'form': form,
                               'add': False},
                              context_instance = RequestContext(request))
edit_friend = decorators.login_required(edit_friend)

def delete_friend(request, id):
    """
    Use this function if you want to delete a friend list.
    It takes an ``id`` argument, which is the **friend id**
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    friend = get_object_or_404(FriendPerson, id=id,
                                             friend_of=request.user)
    friend.delete()
    return HttpResponseRedirect(reverse('friendy_show_main_friends'))
delete_friend = decorators.login_required(delete_friend)

###############################################
##
## The following views are used in order to create and/or
## edit your friendlist
##
###############################################

def add_friendlist(request):
    """
    Creates a friendlist that will be elegible for the ``CompositionList``.
    
    **Template:**
    ``friendycontrol/friendlist_form.html``
    
    **Context:**
        ``form``: The form object to render
        
        ``add``: ``True`` if you want to re-mark that is an *add* operation
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`    
    """
    if request.method == 'POST':
        form = FriendListForm(data=request.POST)
        if form.is_valid():
            friendlist = form.save(commit=False)
            friendlist.owner = request.user
            slug = str(slugify(friendlist.group_name))
            friendlist.slug = slug
            try:
                friendlist.save()
            except IntegrityError:
                form.non_field_errors = 'This group name already exist. Please, choose another one.'
            else:
                return HttpResponseRedirect(reverse('friendy_show_main_friendylist'))
    else:
        form = FriendListForm()
    return render_to_response('friendycontrol/friendlist_form.html',
                              {'form': form,
                               'add': True},
                              context_instance = RequestContext(request))
add_friendlist = decorators.login_required(add_friendlist)

def edit_friendlist(request, id):
    """
    Edit a friendlist.
    
    **Template:**
    ``friendycontrol/friendlist_form.html``
    
    **Context:**
        ``form``: The form object to render
        
        ``add``: ``True`` if you want to re-mark that is an *add* operation
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required` 
    """
    try:
        friendlist = get_object_or_404(FriendListGroupName, id=id,
                                                            owner = request.user)
    except Http404:
        raise Http404
    if request.method == "POST":
        form = FriendListForm(instance=friendlist, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('friendy_show_main_friendylist'))
    else:
        form = FriendListForm(instance=friendlist)
    return render_to_response('friendycontrol/friendlist_form.html',
                              {'form': form,
                               'add': False}, 
                              context_instance = RequestContext(request))
edit_friendlist = decorators.login_required(edit_friendlist)

def delete_friendlist(request, id):
    """
    Delete a friendlist.
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required` 
    """
    friendlist = get_object_or_404(FriendListGroupName, id=id,
                                                        owner=request.user)
    friendlist.delete()
    return HttpResponseRedirect(reverse('friendy_show_main_friendylist'))
delete_friendlist = decorators.login_required(delete_friendlist)

###############################################
##
## The following views are used in order to create and/or
## edit your composition
##
###############################################

def add_composition(request):
    """
    Creates a CompositionList by selecting the 
    :class:`FriendListGroupName <friendycontrol.models.FriendListGroupName>` that
    will form this :class:`CompositionList <friendycontrol.models.CompositionList>` object.
    
    **Template:**
    ``friendycontrol/composition_form.html``
    
    **Context:**
        ``form_composition``: a select multiple box
        
        ``form_readable``: a checkbox to mark whether you give
                             or deny the readable permission
                             
        ``form_app``: the application to which you give readable access
        
        ``add``: ``True`` if you want to re-mark that is an *add* operation
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required` 
    """
    if request.method == 'POST':
        form_composition = CompositionListForm(request.user, data=request.POST)
        form_readable = ReadableForm(data=request.POST)
        if form_composition.is_valid() and form_readable.is_valid():
            composition = form_composition.save(commit=False)
            composition.owner = request.user
            #composition.spaces = form_app.perm_space
            composition.save()
            form_composition.save_m2m()
            
            readable = form_readable.save(commit=False)
            readable.foreign_group = composition
            readable.save()
            
            for space in form_composition.cleaned_data['spaces']:
                app = RelationModel()
                app.readable = readable
                app.content_object = space 
                app.save()
            
            return HttpResponseRedirect(reverse('friendy_show_main_compositions'))
    else:
        form_composition = CompositionListForm(request.user)
        form_readable = ReadableForm()
    return render_to_response('friendycontrol/composition_form.html',
                              {'form_composition': form_composition,
                               'form_readable': form_readable,
                               'add': True},
                               context_instance=RequestContext(request))
add_composition = decorators.login_required(add_composition)

def edit_composition(request, id):
    """
    Edits the CompositionList by changing the elements that belongs to it.
    
    **Template:**
    ``friendycontrol/composition_form.html``
    
    **Context:**
        ``form_composition``: a select multiple box
        
        ``form_readable``: a checkbox to mark whether you give
                             or deny the readable permission
                             
        ``form_app``: the application to which you give readable access
        
        ``add``: ``True`` if you want to re-mark that is an *add* operation
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required` 
    """
    try:
        composition_list = get_object_or_404(CompositionList, id=id,
                                                              owner = request.user)
        readable = composition_list.readable_set.get(foreign_group=composition_list.id)
        relationmodel_list = readable.relationmodel_set.all()   
    except (Http404, Readable.DoesNotExist, RelationModel.DoesNotExist):
        raise Http404
    
    if request.method == 'POST':
        form_composition = CompositionListForm(request.user,
                                               instance=composition_list,
                                               data = request.POST)
        form_readable = ReadableForm(instance = readable, data = request.POST)
        #form_app = AppForm(request.user, data = request.POST)
        if form_composition.is_valid() and form_readable.is_valid():
            form_composition.save()
            form_readable.save()
            
            for space in form_composition.cleaned_data['spaces']:
                try:
                    # If it exists, then do nothing, since nothing has changed
                    app = get_object_or_404(RelationModel, readable=readable,
                                                           object_id = space.id)
                except Http404:
                    # If it does not exist, then create the new value
                    app = RelationModel()
                    app.readable = readable
                    app.content_object = space 
                    app.save()
            
            # We have created all the elements, but we must delete those that are no
            # longer part of this group
            for element in relationmodel_list:
                try:
                    app = relationmodel_list.get(id=element.id)
                    empty = form_composition.cleaned_data['spaces'].filter(id=app.object_id)
                    
                    if len(empty)==0:
                        app.delete()

                except Space.DoesNotExist:
                    print "Exception: %s" % (element)
                    raise Space.DoesNotExist('Hubo un problema en la app friendycontrol')            
            return HttpResponseRedirect(reverse('friendy_show_main_compositions'))
    else:
        form_composition = CompositionListForm(request.user, instance=composition_list)
        form_readable = ReadableForm(instance = readable)
        
        #initial = {'perm_space':[value[0] for value in relationmodel_list.values_list('object_id')]}
        #form_app = AppForm(request.user, initial)
    return render_to_response('friendycontrol/composition_form.html',
                              {'form_composition': form_composition,
                               'form_readable': form_readable,
                               #'form_app': form_app,
                               'add': False},
                               context_instance=RequestContext(request))
edit_composition = decorators.login_required(edit_composition)

def delete_composition(request, id):
    """
    Deletes the CompositionList and all his dependencies
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required` 
    """
    composition = get_object_or_404(CompositionList, id=id, owner=request.user)
    for readable in composition.readable_set.all():
        for relational_model in readable.relationmodel_set.all():
            relational_model.delete()
        readable.delete()
    composition.delete()
    
    return HttpResponseRedirect(reverse('friendy_show_main_compositions'))
delete_composition = decorators.login_required(delete_composition)
    