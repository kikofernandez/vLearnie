
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'fhy.views.admin.show_root_directory',
        name='fhy_show_root_list'),
    
    url(r'^folder/add/$',
        'fhy.views.forms.add_folder_in_root',
        name='fhy_add_folder_in_root'),
        
    url(r'^file/add/(?P<datatype>[\d])/$',
        'fhy.views.forms.add_file_in_root',
        name='fhy_add_file_in_root'),
        
    url(r'^(?P<folder>[\d]+)/$',
        'fhy.views.admin.show_folder_content',
        name='fhy_show_folder_content_list'),
        
    url(r'^(?P<folder>[\d]+)/folder/add/$',
        'fhy.views.forms.add_folder',
        name='fhy_add_folder'),
    
    url(r'^folder/edit/(?P<folder>[\d]+)/(?P<root>[\d(0|1)])/$',
        'fhy.views.forms.edit_folder',
        name='fhy_edit_folder'),
        
    url(r'^(?P<folder>[\d]+)/file/add/$',
        'fhy.views.forms.add_file',
        name='fhy_add_file'),
    
    url(r'^file/edit/(?P<idfile>[\d]+)/(?P<root>[\d(0|1)])/$',
        'fhy.views.forms.edit_file',
        name='fhy_edit_file'),
    
    url(r'^image/edit/(?P<idimage>[\d]+)/(?P<root>[\d(0|1)])/$',
        'fhy.views.forms.edit_image',
        name='fhy_edit_image'),
        
    url(r'^(?P<folder>[\d]+)/image/add/$',
        'fhy.views.forms.add_image',
        name='fhy_add_image'),
    
    url('^delete/folder/(?P<idfolder>[\d]+)/$',
        'fhy.views.forms.delete_folder',
        name='fhy_delete_folder'),
    
    url('^delete/file/(?P<idfile>[\d]+)/$',
        'fhy.views.forms.delete_file',
        name='fhy_delete_file'),
)