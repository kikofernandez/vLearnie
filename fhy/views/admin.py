from fhy.models import *
from space.models import Space
from django.http import Http404
from django.views.generic.list_detail import object_list
from django.contrib.auth import decorators
from django.shortcuts import get_object_or_404, render_to_response, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

def show_root_directory(request, space_name):
    """
    This view shows the main root folder (similar in Linux to /)
    
    **Template:**
    ``fhy/resources_list.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
        
    **Context-variables:**
        * space: :class:`Space <space.models.Space>`
        * idfolder: Integer (not every Integer is valid, just the one that belongs to the root folder),
        * images: [:class:`ImageFHY <fhy.models.ImageFHY>`], where the list is a list with 
          images that belongs to the appropriate :class:`root <fhy.models.Root>`,
        * files: [:class:`FileFHY <fhy.models.FileFHY>`], where the list is a list with 
          files that belongs to the appropriate :class:`root <fhy.models.Root>`
    
    **Raise:**
        :class:`django.http.Http404` if no :class:`Space <space.models.Space>`
        object exist.
    """
    
    try:
        space = get_object_or_404(Space, user=request.user,
                                 slug=space_name)
        #space = Space.objects.select_related('id','root_set__id').filter(user=request.user).get(slug=space_name)
        #space = Space.objects.select_related(depth=4).filter(user=request.user).get(slug=space_name)
        # There exists just one root for every space
        
#        root = space.root_set.select_related().all()[0]
        root = space.root_set.select_related().all()
        
        if len(root)==0:
            # Create a root directory
            root = Root.objects.create(title="Personal space",
                                slug="personal-space",
                                space=space)
            root.save()          
        else:
            root = root[0]
        
#        kwargs = {'space_name': space_name, 'folder': root.id}
#        return HttpResponseRedirect(reverse('fhy_show_folder_content_list', kwargs=kwargs))
        root_list = root.folders.all()
        image_list = root.images.all()
        file_list = root.files.all()
        return object_list(request,
                           queryset=root_list,
                           extra_context = {'space': space,
                                            'idfolder': root.id,
                                            'images': image_list,
                                            'files': file_list
                                            },
                           template_name='fhy/resources_list.html',)
                           #extra_context)  
    except Space.DoesNotExist:
        raise Http404('Create a root folder please')
show_root_directory = decorators.login_required(show_root_directory)
        

def show_folder_content(request, space_name, folder):
    """
    Shows the content of the folder. Used after you have accessed at least to one folder.
    
    **Templates:**
    ``fhy/folder_contents.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
        
    **Context Variables:**
        * space: :class:`Space <space.models.Space>`
        * idfolder: Integer (not every Integer is valid, just the one that belongs to the root folder),
        * images: [:class:`ImageFHY <fhy.models.ImageFHY>`], where the list is a list with 
          images that belongs to the appropriate :class:`root <fhy.models.Root>`,
        * files: [:class:`FileFHY <fhy.models.FileFHY>`], where the list is a list with 
          files that belongs to the appropriate :class:`root <fhy.models.Root>`
        * folders: [:class:`Folder <fhy.models.Folder>`]
    """
    try:
        folders = folder.split('/')
        print folders
        idfolder = folders[-1]
        #space = Space.objects.filter(user=request.user).get(slug=space_name)
        
        folder_list = Folder.objects.filter(object_id = idfolder).filter(content_type__name='folder')
        file_list = FileFHY.objects.filter(object_id = idfolder).filter(content_type__name='folder')
        image_list = ImageFHY.objects.filter(object_id = idfolder).filter(content_type__name='folder')
        
        get_object_or_404(Folder, id=idfolder,
                                  space__slug=space_name)
    except Space.DoesNotExist, Root.DoesNotExist:
        raise Http404('You are not the owner of this file')
    except Http404:
        raise Http404('The folder you are looking for does not exist')
    return object_list(request, 
                       queryset = file_list,
                       extra_context = {'folders': folder_list,
                                        'space': Space.objects.get(user=request.user,
                                                                   slug = space_name),
                                        'images': image_list,
                                        'files': file_list,
                                        'idfolder': idfolder},
                       template_name = 'fhy/folder_contents.html')
#    return render_to_response('fhy/folder_contents.html',
#                              {'id': idfolder})
show_folder_content = decorators.login_required(show_folder_content)