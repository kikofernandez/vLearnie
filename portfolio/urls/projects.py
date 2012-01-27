from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'portfolio.views.admin.manage_project',
        name='portfolio_manage_portfolio'),
        
    url(r'^add/$',
        'portfolio.views.admin.create_project',
        name='portfolio_create_project'),
    
    url(r'^edit/(?P<id>\d+)/$',
        'portfolio.views.admin.edit_project',
        name='portfolio_edit_project'),
    
    url(r'^delete/(?P<id>\d+)/$',
        'portfolio.views.admin.delete_project',
        name='portfolio_delete_project'),
)