from django.conf.urls.defaults import *

urlpatterns= patterns('',
    # I already has account//community/
    url(r'^$',
      'community.views.communities.community_index',
      name='community_index_communities'),
    
    url(r'^add/$',
        'community.views.forms.add_community',
        name='community_community_add_community'),
    
    url(r'^(?P<community>[-\w]+)/$',
        'community.views.forms.admin_index',
        name='community_community_admin_index'),
    
    url(r'^(?P<community>[-\w]+)/add/resource/$',
        'community.views.forms.create_resource',
        name='community_resource_create_resource'),
    
    url(r'^(?P<community>[-\w]+)/edit/(?P<id>\d+)/$',
        'community.views.forms.edit_resource',
        name='community_resource_edit_resource'),
    
    url(r'^(?P<community>[-\w]+)/delete/(?P<id>\d+)/$',
        'community.views.forms.delete_resource',
        name='community_resource_delete_resource'),
    
)