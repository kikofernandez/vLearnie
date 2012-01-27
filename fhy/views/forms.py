from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib.auth import decorators
from fhy.forms import FolderForm, FileFHYForm, ImageFHYForm, CommunityFileForm
from fhy.models import *
from space.models import Space
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import Http404
from community.models import Community #URLCommunityResource,
#from community.models.Resource import STATUS_TYPE
from datetime import date
#from community.models import URL, Resource
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.datastructures import MultiValueDictKeyError

PDF = 0
IMAGE = 1
FORMAT_TYPES = (PDF, IMAGE)

def add_file_in_root(request, space_name, datatype):
    """
    This view will create files in the root directory
    
    **Arguments:** 
        * request: Request object
        * space_name: string containing the space_name to which belongs this file
    
    **Template:**
        * ``fhy/fhy_file_form.html``
        * Reverse: `fhy_show_root_list`
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    space = get_object_or_404(Space, user=request.user,
                                     slug=space_name) 
    
    # Since this template is used for either Files and Images, we must
    # determine which template to apply since the beginning
    if int(datatype) == PDF:
        template = 'fhy/fhy_file_form.html'
    elif int(datatype) == IMAGE:
        template = 'fhy/fhy_image_form.html'
    else:
        raise Http404("Invalid page")
    
    if request.method == 'POST':
        if int(datatype) == PDF:
            form = FileFHYForm(request.POST, request.FILES)
        elif int(datatype) == IMAGE:
            form = ImageFHYForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                new_file = form.save(commit=False)
                handle_uploaded_file(request.FILES['file'])
#                if int(datatype) == PDF:
#                    handle_uploaded_file(request.FILES['file'])
#                elif int(datatype) == IMAGE:
#                    handle_uploaded_file(request.FILES['file'])
                
                new_file.space = space
                new_file.pub_date = date.today()
                                #Space.objects.filter(user=request.user).get(slug=space_name)
                
                content_type = ContentType.objects.select_related().get(name='root')
                new_file.content_type = content_type
                
                root = Root.objects.select_related().get(space=new_file.space)
                new_file.object_id = root.id
                
                new_file.object_id = root.id
                new_file.save()
                form.save_m2m()
                
                args = [space_name,]
                return HttpResponseRedirect(reverse('fhy_show_root_list', args=args))
        except IntegrityError:
            form.non_field_errors = '''Error, another file with the same 
                                        title exist. Please select another title.'''
    else:
        if int(datatype) == PDF:
            form = FileFHYForm()
            template = 'fhy/fhy_file_form.html'
        elif int(datatype) == IMAGE:
            form = ImageFHYForm()
            template = 'fhy/fhy_image_form.html'
        else:
            raise Http404("Invalid page")
    return render_to_response(template,
                              {'form': form,
                               'space': space,
                               'add': True},
                              context_instance= RequestContext(request))
add_file_in_root = decorators.login_required(add_file_in_root)

def add_folder_in_root(request, space_name):
    """
    This view will create folders in the root directory
    
    **Arguments:** 
        * request: Request object
        * space_name: string containing the space_name to which belongs this folder
    
    **Template:**
    ``fhy/fhy_form.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    space = get_object_or_404(Space, slug=space_name,user=request.user)
    if request.method == 'POST':
        form = FolderForm(data=request.POST)
        try:
            if form.is_valid():
                new_folder = form.save(commit=False)
                new_folder.space = space
               
                content_type = ContentType.objects.select_related().get(name='root')
                new_folder.content_type = content_type
                
                root = Root.objects.select_related().get(space=new_folder.space)
                new_folder.object_id = root.id
                new_folder.save()
                form.save_m2m()
                
                return HttpResponseRedirect(reverse('fhy_show_root_list', args=[space_name]))
        except IntegrityError:
            form.non_field_errors = '''Error, another folder with the same 
                                        title exist. Please select another title.'''
    else:
        form = FolderForm()
    return render_to_response('fhy/fhy_form.html',
                              {'form': form,
                               'space': space,
                               'add': True},
                              context_instance = RequestContext(request))
add_folder_in_root = decorators.login_required(add_folder_in_root)



def add_folder(request, space_name, folder):
    """
    Create a new folder inside a previous created folder.
    
    **Arguments:**
        * request: Request object
        * space_name: string containing the space_name to which belongs this folder
        * folder: integer number that contains who is the parent folder
    
    **Templates:**
        ``fhy/fhy_form.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    space = get_object_or_404(Space, user=request.user,
                                     slug=space_name)    
    
    if request.method == 'POST':
        try:
            # The id must exist, and we also use content_type in order get if there
            # exists at least one folder and not the root folder. Due to we use
            # content_types, we could also retrieve the root folder (we don't want this)
            get_object_or_404(Folder, id=folder,
                                      content_type__name='folder',
                                      )
        except Http404:
            try: 
                get_object_or_404(Folder, id=folder,
                                          content_type__name='root',)
            except Http404:
                raise Http404('No folder exists with that name')

        form = FolderForm(data = request.POST)
        
        try:
            if form.is_valid():
    
                new_folder = form.save(commit=False)
                new_folder.space = space
               
                content_type = ContentType.objects.select_related().get(name='folder')
                new_folder.content_type = content_type
                
                new_folder.object_id = int(folder.split('/')[0])
                new_folder.save()
                form.save_m2m()
                args = [space_name, folder]
                return HttpResponseRedirect(reverse('fhy_show_folder_content_list', args=args))
        except IntegrityError:
            form.non_field_errors = '''Error, another folder with the same 
                                        title exist. Please select another title.'''
    else:
        form = FolderForm()
    return render_to_response('fhy/fhy_form.html',
                              {'form': form,
                               'space': space},
                              context_instance = RequestContext(request))
add_folder = decorators.login_required(add_folder)

def edit_folder(request, space_name, folder, root=False):
    """
    View that edits an existing folder (no matter whether is a root folder or not).
    
     **Arguments:**
        * request: Request object
        * space_name: string containing the space_name to which belongs this folder
        * folder: integer number id that points to the folder we want to change
        * root: `0` or `1` indicating whether this folder belongs to the root folder
    
    **Templates:**
        * ``fhy_form.html``
        
        **Reverse:**
            * ``fhy_show_root_list``: returns to the root folder
            * ``fhy_show_folder_content_list``: returns to the folder indicated
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    folder_object = get_object_or_404(Folder, id=folder)
    root = bool(int(root))    
    
    if request.method == 'POST':
        form = FolderForm(data=request.POST, instance=folder_object)
        try:
            if form.is_valid():
                form.save()
                args = [space_name]
                if root:
                    template = 'fhy_show_root_list'
                else:
                    template = 'fhy_show_folder_content_list'
                    args.append(folder)
                return HttpResponseRedirect(reverse(template, args=args))
        except IntegrityError:
                form.non_field_errors = '''Error, another folder with the same 
                                            title exist. Please select another title.'''
    else:
        form = FolderForm(instance=folder_object)
    return render_to_response('fhy/fhy_form.html',
                              {'form': form,
                               'space': folder_object.space},
                              context_instance = RequestContext(request))
edit_folder = decorators.login_required(edit_folder)

def handle_uploaded_file(f):
    """
    This function will upload a file
    """
    destination = open(f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()



def add_file(request, space_name, folder):
    """
    This function will upload a file inside the folder ``folder``.
    
     **Arguments:**
        * request: Request object
        * space_name: string containing the space_name to which belongs this folder
        * folder: integer number that contains the parent folder (dentro de que folder reside)
    
    **Templates:**
        ``fhy/fhy_file_form.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    space = get_object_or_404(Space, user=request.user,
                                     slug=space_name) 
    if request.method == 'POST':
        form = FileFHYForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                new_file = form.save(commit=False)
                
                # when doing form.save, it relates the form.file with new_file.file
                handle_uploaded_file(request.FILES['file'])
                new_file.space = space
                new_file.pub_date = date.today()
                
                content_type = ContentType.objects.select_related().get(name='folder')
                new_file.content_type = content_type
                
                new_file.object_id = int(folder.split('/')[0])
                new_file.save()
                form.save_m2m()
                
                args = [space_name, folder]
                return HttpResponseRedirect(reverse('fhy_show_folder_content_list', args=args))
        except IntegrityError:
            form.non_field_errors = '''Error, another file with the same 
                                        title exist. Please select another title.'''
        except MultiValueDictKeyError:
            form.non_field_errors = 'Please, you must submit a file.'
    else:
        form = FileFHYForm()
    return render_to_response('fhy/fhy_file_form.html',
                              {'form': form,
                               'space': space,
                               'add': True},
                              context_instance= RequestContext(request))
add_file = decorators.login_required(add_file)

def edit_file(request, space_name, idfile, root=0):
    """
    This function will allow you to update a file inside the folder ``folder``. It edits 
    also a :class:`URLCommunityResource <community.models.URLCommunityResource>` existing
    object.
    
     **Arguments:**
        * request: Request object
        * space_name: string containing the space_name to which belongs this folder
        * idfolder: integer number that contains the parent folder (dentro de que folder reside)
    
    **Templates:**
        ``fhy/fhy_file_form.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    
    file_object = get_object_or_404(FileFHY, space__slug=space_name,
                                             id = idfile)
    space = get_object_or_404(Space, user=request.user,
                                     slug=space_name)
    root = bool(int(root))
    if request.method == 'POST':
        form = FileFHYForm(request.POST, request.FILES, instance=file_object)
        try:
            if form.is_valid():
                form.save(commit=False)
                
                # This condition ensures that there are always a file associated.
                # We cannot do it in def clean_file since we wouldn't be able to check
                # the existence of a previous file. In this case, since we are editing,
                # there must have been a previous file or adD_file would have raised an
                # alert.
                if request.FILES:
                    #file_object.file.delete()
                    handle_uploaded_file(request.FILES['file'])
                file_object.pub_date = date.today()
                file_object.save()
                form.save_m2m()
                
                args = [space_name]
                if root:
                    template = 'fhy_show_root_list'
                else:
                    args.append(file_object.content_object.id)
                    template = 'fhy_show_folder_content_list'
                
                return HttpResponseRedirect(reverse(template, args=args))
        except MultiValueDictKeyError:
            form.non_field_errors = 'Please, you must submit a file.'
    else:
        form = FileFHYForm(instance=file_object)
    return render_to_response('fhy/fhy_file_form.html',
                              {'form': form,
                               'space': space,
                               'add': False},
                               context_instance= RequestContext(request))
edit_file = decorators.login_required(edit_file)



def add_image(request, space_name, folder):
    space = get_object_or_404(Space, user=request.user,
                                     slug=space_name)
    
    if request.method == 'POST':
        form = ImageFHYForm(request.POST, request.FILES)
        
        try:
            print "Image valid? %s" % form.is_valid()
            if form.is_valid():
                new_image = form.save(commit=False)
                handle_uploaded_file(request.FILES['file'])
                
                new_image.space = space #Space.objects.filter(user=request.user).get(slug=space_name)
                new_image.pub_date = date.today()
                content_type = ContentType.objects.select_related().get(name='folder')
                new_image.content_type = content_type
                new_image.object_id = int(folder.split('/')[0])
                new_image.save()
                form.save_m2m()
                
                args = [space_name, folder]
                return HttpResponseRedirect(reverse('fhy_show_folder_content_list', args=args))
        except IntegrityError:
            form.non_field_errors = '''Error, another image with the same 
                                        title exist. Please select another title.'''
            
    else:
        form = ImageFHYForm()
    return render_to_response('fhy/fhy_image_form.html',
                              {'form': form,
                               'space': space,
                               'add': True},
                              context_instance = RequestContext(request))
add_image = decorators.login_required(add_image)


def edit_image(request, space_name, idimage, root=0):
    """
    This function will allow you to update a file inside the folder ``folder``. It edits 
    also a :class:`URLCommunityResource <community.models.URLCommunityResource>` existing
    object.
    
     **Arguments:**
        * request: Request object
        * space_name: string containing the space_name to which belongs this folder
        * idfolder: integer number that contains the parent folder (dentro de que folder reside)
    
    **Templates:**
        ``fhy/fhy_file_form.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    
    image_object = get_object_or_404(ImageFHY, space__slug=space_name,
                                               id = idimage)
    space = get_object_or_404(Space, user=request.user,
                                     slug=space_name)
    root = bool(int(root))
    if request.method == 'POST':
        form = ImageFHYForm(request.POST, request.FILES, instance=image_object)
        try:
            if form.is_valid():
                form.save(commit=False)
                
                # This condition ensures that there are always a file associated.
                # We cannot do it in def clean_file since we wouldn't be able to check
                # the existence of a previous file. In this case, since we are editing,
                # there must have been a previous file or adD_file would have raised an
                # alert.
                if request.FILES:
                    #file_object.file.delete()
                    handle_uploaded_file(request.FILES['file'])
                image_object.pub_date = date.today()
                image_object.save()
                form.save_m2m()
                
                args = [space_name]
                if root:
                    template = 'fhy_show_root_list'
                else:
                    args.append(image_object.content_object.id)
                    template = 'fhy_show_folder_content_list'
                
                return HttpResponseRedirect(reverse(template, args=args))
        except MultiValueDictKeyError:
            form.non_field_errors = 'Please, you must submit a file.'
    else:
        form = ImageFHYForm(instance=image_object)
    return render_to_response('fhy/fhy_image_form.html',
                              {'form': form,
                               'space': space,
                               'add': False,
                               'current': image_object},
                               context_instance= RequestContext(request))
edit_image = decorators.login_required(edit_image)



def delete_file(request, space_name, idfile):
    """
    **Arguments:**
        * request: Request object
        * space_name: string containing the space_name to which belongs this folder
        * idfile: integer number indicating which file must be deleted
    
    **Templates Reverse:**
        * ``fhy_show_root_list``: returns to the root folder
        * ``fhy_show_folder_content_list``: returns to the folder indicated
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    file = get_object_or_404(FileFHY, id=idfile,
                                      space__slug = space_name,
                                      space__user = request.user)
    folder = file.content_object
    file.delete()
    args = [space_name]
    if folder.__class__ == Root:
        template = 'fhy_show_root_list'
    else: 
        template = 'fhy_show_folder_content_list'
        args.append(folder.id)
    return HttpResponseRedirect(reverse(template, args=args))
delete_file = decorators.login_required(delete_file)

def delete_recursive_folder(folder_object, space_name):
    """
    Recursive case for a recursive function, using backtracking.
    """
    folders = Folder.objects.filter(object_id = folder_object.id,
                                    content_type__name = folder_object.__class__.__name__.lower())

    for folder in folders:
        delete_recursive_folder(folder, space_name)
        folder.delete()
    
    FileFHY.objects.filter(object_id=folder_object.id,
                           content_type__name = folder_object.__class__.__name__.lower()).delete()
    
    ImageFHY.objects.filter(object_id=folder_object.id,
                            content_type__name = folder_object.__class__.__name__.lower()).delete()

def delete_base_folder(space_name, idfolder):
    """
    Base case for a recursive function, using backtracking.
    """
    folder_object = get_object_or_404(Folder, id=idfolder,
                                              space__slug = space_name)
    
    folders = Folder.objects.filter(object_id = idfolder,
                                    content_type__name = folder_object.__class__.__name__.lower())

    for folder in folders:
        delete_recursive_folder(folder, space_name)
        folder.delete()
    
    FileFHY.objects.filter(object_id=idfolder,
                           content_type__name=folder_object.__class__.__name__.lower()).delete()
    ImageFHY.objects.filter(object_id=idfolder,
                            content_type__name=folder_object.__class__.__name__.lower()).delete()
    
def delete_folder(request, space_name, idfolder):
    """
    Deletes folders recursively. This means that any other folder /files / images
    inside this folder will be removed
    
    **Arguments:**
        * request: Request object
        * space_name: string containing the space_name to which belongs this folder
        * idfolder: integer number of the folder to delete
    
    **Templates Reverse:**
        * ``fhy_show_root_list``: returns to the root folder
        * ``fhy_show_folder_content_list``: returns to the folder indicated
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
    """
    # Checks that the delete order has been sent by the owner of the folder
    # + get the folder
    folder_object = get_object_or_404(Folder, id=idfolder,
                                              space__slug = space_name,
                                              space__user = request.user)
    delete_base_folder(space_name, idfolder)
    args = [space_name]
    
    if folder_object.content_type.name == 'root':
        # if we are deleting a root folder, then redirect to the apropriate view
        template = 'fhy_show_root_list'
    else:
        template = 'fhy_show_folder_content_list'
        args.append(folder_object.content_object.id)
    folder_object.delete()
    return HttpResponseRedirect(reverse(template, args=args))
delete_folder = decorators.login_required(delete_folder)
