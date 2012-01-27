from space.models import Space
from coltrane.models import Category, Entry
from space.forms import CategoryForm
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
#from django.core.exceptions import ObjectDoesNotExist 
from space.exceptions import DuplicateValuesAreNotUnique
from django.shortcuts import HttpResponseRedirect, render_to_response, get_object_or_404, Http404
from django.contrib.auth import decorators
from django.template import RequestContext

def add_category(request, space_name):
    if request.method == 'POST':
        form = CategoryForm(data = request.POST)
        try:
            if form.is_valid():
                new_category = form.save(commit=False)
                new_category.space = Space.objects.filter(user = request.user).get(slug=space_name)
                new_category.author = request.user
                new_category.save()
                kwargs = {'space_name':new_category.space.slug}
                return HttpResponseRedirect(reverse('space_space_list_objects',kwargs=kwargs))
        except DuplicateValuesAreNotUnique:
            form.non_field_errors = "The title of this space already exist. Please choose another one."
    else:
        form = CategoryForm()
    return render_to_response('space/category_form.html',
                              {'form': form,
                               'space': Space.objects.filter(user=request.user).get(slug=space_name),
                               'user': request.user,
                               'add': True},
                               context_instance=RequestContext(request))
add_category = decorators.login_required(add_category)

def edit_category(request, space_name, slug_category):
    try:
        space = Space.objects.filter(user=request.user).get(slug=space_name)
        category = get_object_or_404(space.category_set.all(), slug=slug_category)
    except Space.DoesNotExist:
        print "No hay categorias que cuadren."
        raise Http404
    if request.method == 'POST':
        form = CategoryForm(instance=category, data = request.POST)
        if form.is_valid():
            form.save()
            kwargs = {'space_name': space_name}
            return HttpResponseRedirect(reverse('space_space_list_objects', kwargs=kwargs))
    else:
        form = CategoryForm(instance=category)
    return render_to_response('space/category_form.html',
                              {'form': form,
                               'space': Space.objects.filter(user=request.user).get(slug=space_name),
                               'user': request.user,
                               'add': False},
                               context_instance=RequestContext(request))
edit_category = decorators.login_required(edit_category)  

def delete_category(request, space_name, id):
    category = get_object_or_404(Category, space__slug=space_name,
                                           id = id)
    category.delete()
    kwargs = {'space_name': space_name}
    return HttpResponseRedirect(reverse('space_space_list_objects', kwargs=kwargs))
delete_category = decorators.login_required(delete_category)

def show_user_category(request, space_name):
    space = Space.objects.filter(user=request.user).get(slug=space_name)
    categories = space.category_set.all()
    #entry = space.entry_set.all()
#    categories = set()
#    for element in entry.all():
#        categories.update(element.categories.all())
     
    return object_list( request,
                        queryset = categories,
                        template_name = 'space/categories_by_space.html',
                        extra_context = {'user': request.user,
                                         'space': space})   
#    return category_list(request,
#                       set=categories, 
#                       template_name='space/categories_by_space.html', 
#                       extra_context = {'user': request.user,
#                                        'space': space},
#                       )
show_user_category = decorators.login_required(show_user_category)

#def category_list(request, set=None, 
#                  template_name='space/categories_by_space.html', extra_context=None):
    
    