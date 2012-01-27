from django.shortcuts import render_to_response, HttpResponseRedirect,\
    get_object_or_404
from django.contrib.auth import decorators
from community.forms import CommunityForm, ResourceForm#EntryForm, URLForm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from community.models import Community, Resource
from django.http import Http404


def admin_index(request, community):
    resources = []
    try: 
        resources = Resource.objects.filter(author = request.user,
                                            community__slug = community).order_by('-pub_date')
    except Http404:
        resources = []
    finally:
        return render_to_response('community/admin_archive_index.html',
                                  {'resources': resources,
                                   'community': community},
                                  context_instance = RequestContext(request))

# We do not want to allow edit the community since nobody is the
# the administrator of it.

def add_community(request):
    """
    This view creates a community.
    
    **Template:**
    ``community/community_form.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
        
    **Context-variables:**
        * form: the form itself
        * add: boolean value that tells the template whether to show ``add`` or ``edit``
    
    """
    if request.method == 'POST':
        form = CommunityForm(data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('community_index_communities'))
    else:
        form = CommunityForm()
    return render_to_response('community/community_form.html',
                              {'form': form,
                               'add': True},
                              context_instance=RequestContext(request))
add_community = decorators.login_required(add_community)

def create_resource(request, community):
    """
    This view creates a new resource / entry.
    
    **Template:**
    ``community/resource_form.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
        
    **Context-variables:**
        * form: the form itself
        * add: boolean value that tells the template whether to show ``add`` or ``edit``
    
    """
    if request.method == 'POST':
        form = ResourceForm(data = request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = request.user
            resource.community = Community.objects.get(slug=community)
            resource.save()
            kwargs = {'community': community}
            return HttpResponseRedirect(reverse('community_community_admin_index', kwargs=kwargs))
    else:
        form = ResourceForm()
    return render_to_response('community/resource_form.html',
                              {'form': form,
                               'community': community,
                               'add': True},
                               context_instance=RequestContext(request))
create_resource = decorators.login_required(create_resource)

def edit_resource(request, community, id):
    """
    This view edits an existing resource / entry.
    
    **Template:**
    ``community/resource_form.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
        
    **Context-variables:**
        * form: the form itself
        * add: boolean value that tells the template whether to show ``add`` or ``edit``
    
    """
    resource = get_object_or_404(Resource, author = request.user,
                                           community__slug = community,
                                           id = id)
    if request.method == 'POST':
        form = ResourceForm(instance = resource, data = request.POST)
        if form.is_valid():
            form.save()
            kwargs = {'community': community}
            return HttpResponseRedirect(reverse('community_community_admin_index', kwargs=kwargs))
    else:
        form = ResourceForm(instance=resource)
    return render_to_response('community/resource_form.html',
                              {'form': form,
                               'community': community,
                               'add':False},
                               context_instance=RequestContext(request))
edit_resource = decorators.login_required(edit_resource)

def delete_resource(request, community, id):
    """
    This view deletes an existing resource / entry.
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    
    """
    resource = get_object_or_404(Resource, author = request.user,
                                           community__slug = community,
                                           id = id)
    resource.delete()
    kwargs = {'community': community}
    return HttpResponseRedirect(reverse('community_community_admin_index'), kwargs=kwargs)
delete_resource = decorators.login_required(delete_resource)