from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url(r'^$',
        'portfolio.views.admin.personal_main',
        name='portfolio_main_personal'),
    
    url(r'^add/$',
        'portfolio.views.admin.create_personal',
        name='portfolio_create_personal'),
    
    url(r'^edit/$',
        'portfolio.views.admin.edit_personal',
        name='portfolio_edit_personal'),
    
    url(r'^delete/$',
        'portfolio.views.admin.delete_personal',
        name='portfolio_delete_personal'),
)