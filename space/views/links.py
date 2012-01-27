from space.models import Space
from coltrane.models import Category, Entry, Link
from space.forms import LinkForm
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
#from django.core.exceptions import ObjectDoesNotExist 
from space.exceptions import DuplicateValuesAreNotUnique
from django.shortcuts import HttpResponseRedirect, render_to_response, get_object_or_404, Http404
from django.contrib.auth import decorators
from django.template import RequestContext

def add_link(request, space_name):
    """
    This function creates a new link associated with the logged in user
    
    **Type:**
        * private
    
    **Arguments:** 
        * request: Request object
        * space_name: string containing the space_name to which belongs this file
    
    **Template:**
        * ``space/link_form.html``
    
    **Context-variables:**
        * ``form``: the form itself
        * ``space``: the corresponding :class:`Space <space.models.Space> object
        * ``user``: the given username
        * ``add``: boolean value
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    if request.method == 'POST':
        form = LinkForm(data = request.POST)
        try:
            if form.is_valid():
                new_link = form.save(commit=False)
                new_link.space = Space.objects.filter(user = request.user).get(slug=space_name)
                new_link.posted_by = request.user
                new_link.save()
                kwargs = {'space_name':new_link.space.slug}
                return HttpResponseRedirect(reverse('space_space_list_objects',kwargs=kwargs))
        except DuplicateValuesAreNotUnique:
            form.non_field_errors = "This link already exists."
    else:
        form = LinkForm()
    return render_to_response('space/link_form.html',
                              {'form': form,
                               'space': Space.objects.filter(user=request.user).get(slug=space_name),
                               'user': request.user,
                               'add': True},
                               context_instance=RequestContext(request))
add_link = decorators.login_required(add_link)

def edit_link(request, space_name, slug_link):
    try:
        space = Space.objects.filter(user=request.user).get(slug=space_name)
        link = get_object_or_404(space.link_set.all(), slug=slug_link)
        #space.category_set.get(title=slug_category)
        #category = Category.objects.filter(space__slug=space_name).filter(categories__slug=slug_category)
    except Space.DoesNotExist:
        print "No hay links que cuadren."
        raise Http404
    if request.method == 'POST':
        form = LinkForm(instance=link, data = request.POST)
        if form.is_valid():
            form.save()
            kwargs = {'space_name': space_name}
            return HttpResponseRedirect(reverse('space_space_list_objects', kwargs=kwargs))
    else:
        form = LinkForm(instance=link)
    return render_to_response('space/link_form.html',
                              {'form': form,
                               'space': Space.objects.filter(user=request.user).get(slug=space_name),
                               'user': request.user,
                               'add': False},
                               context_instance=RequestContext(request))
edit_link = decorators.login_required(edit_link)  

def delete_link(request, space_name, id):
    link = get_object_or_404(Link, posted_by=request.user,
                                   id = id)
    link.delete()
    kwargs = {'space_name': space_name}
    return HttpResponseRedirect(reverse('space_space_list_links_objects', kwargs=kwargs))
delete_link = decorators.login_required(delete_link)

def show_user_link(request, space_name):
    space = Space.objects.filter(user=request.user).get(slug=space_name)
    links = space.link_set.all()
     
    return object_list( request,
                        queryset = links,
                        template_name = 'space/links_by_space.html',
                        extra_context = {'user': request.user,
                                         'space': space})   
show_user_link = decorators.login_required(show_user_link)

