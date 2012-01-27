from space.models import Space
from coltrane.models import Category
from community.models import Community
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth import decorators
from django.core.urlresolvers import reverse
from space.exceptions import DuplicateValuesAreNotUnique
from coltrane.models import Entry
from space.forms import EntryForm
from django.http import Http404
from django.template import RequestContext

def add_entry(request, space_name):
    categoryset = Category.objects.filter(author=request.user).filter(space__slug=space_name)
    if request.method == 'POST':
        form = EntryForm(categoryset, data=request.POST)
        try:
            if form.is_valid():
                new_entry = form.save(commit=False)
                new_entry.author = request.user
                new_entry.space = Space.objects.filter(user=request.user).get(slug=space_name)
                valid = new_entry.space.entry_set.filter(slug=new_entry.slug)
                if len(valid):
                    raise DuplicateValuesAreNotUnique
                new_entry.save()
                form.save_m2m()
                kwargs = {'space_name': new_entry.space.slug}
                return HttpResponseRedirect(reverse('space_space_list_objects', kwargs=kwargs))
        except DuplicateValuesAreNotUnique:
            form.non_field_errors = 'The entry title is duplicated. Please choose another title'
    else:
#        space = Space.objects.filter(user=request.user).get(slug=space_name)
#        categoryset = space.category_set.all()
        
        #communityset = Community.objects.select_related(depth=2)
        #categoryset = Category.objects.filter(author=request.user).filter(space__slug=space_name)
        form = EntryForm(categoryset)
        #print "Categoryset: %s" % [category.title for category in categoryset]
        #form = EntryForm(categoryset, communityset)
        
    return render_to_response('space/entry_form.html',
                              {'form': form,
                               'space': Space.objects.filter(user=request.user).get(slug=space_name),
                               'user': request.user,
                               'add': True},
                               context_instance=RequestContext(request))
add_entry = decorators.login_required(add_entry)
 
def edit_entry(request, space_name, slug_entry):
    #space_object = Space.objects.filter(user=request.user).get(slug=space_name)
    #space.entry_set.get(slug=slug_entry)
    try:
        entry = get_object_or_404(Entry, author= request.user,
                                         space__slug = space_name,
                                         slug = slug_entry)
        categoryset = Category.objects.filter(author=request.user,
                                              space__slug=space_name)
    except Http404:
        print "No hay entradas que cuadren."
        raise Http404
    if request.method == 'POST':
        form = EntryForm(instance=entry, data = request.POST)
        if form.is_valid():
            form.save()
            kwargs = {'space_name': space_name}
            return HttpResponseRedirect(reverse('space_space_list_objects', kwargs=kwargs))
    else:
        categoryset = Category.objects.filter(author=request.user,
                                              space__slug=space_name)
        form = EntryForm(instance=entry, categoryset=categoryset)
        #print "Primera entrada"
    return render_to_response('space/entry_form.html',
                              {'form': form,
                               'space': Space.objects.filter(user=request.user).get(slug=space_name),
                               'user': request.user,
                               'add': False},
                               context_instance=RequestContext(request))
edit_entry = decorators.login_required(edit_entry)    

def delete_entry(request, space_name, id):
    entry = get_object_or_404(Entry, id = id)
    entry.delete()
    kwargs = {'space_name': space_name}
    return HttpResponseRedirect(reverse('space_space_list_objects', kwargs=kwargs))
delete_entry = decorators.login_required(delete_entry)

def show_user_blog(request, space_name):
    space = Space.objects.filter(slug=space_name).get(user=request.user)
    blog = space.entry_set.all()
    return object_list(request,
                       queryset=blog, 
                       template_name='space/entries_by_blogspace.html', 
                       extra_context = {'user': request.user,
                                        'space': space})
show_user_blog = decorators.login_required(show_user_blog)