from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<username>[-\w]+)/$',
        'portfolio.views.public.category_list',
        name = 'portfolio_category_list'),

    url(r'^(?P<username>[-\w]+)/bio/$',
        'portfolio.views.public.bio_detail',
        name='portfolio_bio_detail'),

    url(r'^(?P<username>[-\w]+)/category/(?P<slug>[-\w]+)/$',
        'portfolio.views.public.category_detail',
        name = 'portfolio_category_detail',
        ),

    url(r'^(?P<username>[-\w]+)/project/(?P<slug>[-\w]+)/$',
        'portfolio.views.public.project_detail',
        name = 'portfolio_project_detail'),

    url(r'^(?P<username>[-\w]+)/skill/(?P<slug>[-\w]+)/$',
        'portfolio.views.public.skill_detail',
        name = 'portfolio_skill_detail'),       
)
