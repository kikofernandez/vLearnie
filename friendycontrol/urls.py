from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'friendycontrol.views.show_main_friendylist',
        name='friendy_show_main_friendylist'),
    
    url(r'^friend/$',
        'friendycontrol.views.show_main_friends',
        name='friendy_show_main_friends'),
        
    url(r'^composition/$',
        'friendycontrol.views.show_main_compositions',
        name='friendy_show_main_compositions'),
       
    url(r'add/friend/$',
        'friendycontrol.views.add_friend',
        name='friendy_add_friend'),
        
    url(r'^edit/friend/(?P<id>[\d]+)/$',
        'friendycontrol.views.edit_friend',
        name='friendy_edit_friend'),
    
    url(r'^delete/friend/(?P<id>[\d]+)/$',
        'friendycontrol.views.delete_friend',
        name='friendy_delete_friend'),
        
    url(r'^add/friendlist/$',
        'friendycontrol.views.add_friendlist',
        name='friendy_add_friendlist'),
    
    url(r'^edit/friendlist/(?P<id>[\d]+)/$',
        'friendycontrol.views.edit_friendlist',
        name='friendy_edit_friendlist'),
        
    url(r'^delete/friendlist/(?P<id>[\d]+)/$',
        'friendycontrol.views.delete_friendlist',
        name='friendy_delete_friendlist'),
    
    url(r'^add/composition/$',
        'friendycontrol.views.add_composition',
        name='friendy_add_composition'),
        
    url(r'^edit/composition/(?P<id>[\d]+)/$',
        'friendycontrol.views.edit_composition',
        name='friendy_edit_composition'),
    
    url(r'^delete/composition/(?P<id>[\d]+)/$',
        'friendycontrol.views.delete_composition',
        name='friendy_delete_composition'),
    
)