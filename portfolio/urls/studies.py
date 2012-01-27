from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'portfolio.views.admin.studies_main',
        name='portfolio_main_studies'),
    
    url(r'^add/$',
        'portfolio.views.admin.create_studies',
        name='portfolio_create_studies'),
    
    url(r'^edit/(?P<id>\d+)/$',
        'portfolio.views.admin.edit_studies',
        name='portfolio_edit_studies'),
    
    url(r'^delete/(?P<id>\d+)/$',
        'portfolio.views.admin.delete_studies',
        name='portfolio_delete_studies')
    
)