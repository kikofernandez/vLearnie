from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'portfolio.views.admin.skill_main',
        name='portfolio_main_skill'),
    
    url(r'^add/$',
        'portfolio.views.admin.create_skill',
        name='portfolio_create_skill'),
    
    url(r'^edit/(?P<id>\d+)/$',
        'portfolio.views.admin.edit_skill',
        name='portfolio_edit_skill'),
    
    url(r'^delete/(?P<id>\d+)/$',
        'portfolio.views.admin.delete_skill',
        name='portfolio_delete_skill'),
)