from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # your available spaces
    url(r'^$',
        'space.views.spaces.show_my_spaces',
        name='space_space_list_spaces'),
    # user create space
    url(r'^add/$',
       'space.views.spaces.create_space',
       name='space_space_create_space'),
       
    url(r'edit/(?P<id>\d+)/$',
      'space.views.spaces.edit_space',
      name='space_space_edit_space'),
    
    url(r'^(?P<space_name>[-\w]+)/$',
        'space.views.spaces.show_user_space',
        name='space_space_list_objects'),
        
    url(r'^(?P<space_name>[-\w]+)/files/',
        include('fhy.urls.admin')),
        
    
    url(r'^(?P<space_name>[-\w]+)/categories/$',
        'space.views.categories.show_user_category',
        name='space_space_list_category_objects'),
        
    url(r'^(?P<space_name>[-\w]+)/categories/add/$',
        'space.views.categories.add_category',
        name='space_space_create_category'),
        
    url(r'^(?P<space_name>[-\w]+)/categories/edit/(?P<slug_category>[-\w]+)/$',
        'space.views.categories.edit_category',
        name='space_space_edit_category'),
    
    url(r'^(?P<space_name>[-\w]+)/categories/delete/(?P<id>\d+)/$',
        'space.views.categories.delete_category',
        name='space_space_delete_category'),
    
#  In case of error, it's because this used to work and now I don't
#  see the point of keeping it.    
    url(r'^(?P<space_name>[-\w]+)/blog/$',
        'space.views.entries.show_user_blog',
         name='space_space_list_entry_objects'),
        
    url(r'^(?P<space_name>[-\w]+)/blog/add/$',
        'space.views.entries.add_entry',
        name='space_space_create_entry'),
        
    url(r'^(?P<space_name>[-\w]+)/blog/edit/(?P<slug_entry>[-\w]+)/$',
        'space.views.entries.edit_entry',
        name='space_space_edit_entry'),
        
    url(r'^(?P<space_name>[-\w]+)/blog/delete/(?P<id>[\d]+)/$',
        'space.views.entries.delete_entry',
        name='space_space_delete_entry'),
    
    url(r'^(?P<space_name>[-\w]+)/links/$',
        'space.views.links.show_user_link',
        name='space_space_list_links_objects'),
        
    url(r'^(?P<space_name>[-\w]+)/links/add/$',
        'space.views.links.add_link',
        name='space_space_create_link'),
    
    url(r'^(?P<space_name>[-\w]+)/links/edit/(?P<slug_link>[-\w]+)/$',
        'space.views.links.edit_link',
        name='space_space_edit_link'),
        
    url(r'^(?P<space_name>[-\w]+)/links/delete/(?P<id>\d+)/$',
        'space.views.links.delete_link',
        name='space_space_delete_link'),
    
    url(r'^(?P<space_name>[-\w]+)/tags/$',
        'space.views.tags.show_user_tag',
        name='space_space_list_tags_objects'),
    
    

    # public view
#    (r'^(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$',
#     'space.views.space_detail',
#     'spaces_space_detail'),
)