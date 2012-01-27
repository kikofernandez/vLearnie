from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'portfolio.views.admin.category_main',
        name='portfolio_main_category'),
    
    url(r'^add/$',
        'portfolio.views.admin.create_category',
        name='portfolio_create_category'),
    
    url(r'^edit/(?P<id>\d+)/$',
        'portfolio.views.admin.edit_category',
        name='portfolio_edit_category'),
    
    url(r'^delete/(?P<id>\d+)/$',
        'portfolio.views.admin.delete_category',
        name='portfolio_delete_category'),
)