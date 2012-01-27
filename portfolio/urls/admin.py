
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Projects in the portfolio
    # The first view:manage_portfolio is the main view plus the one
    # for dealing and editing projects                   
        
    # Projects area
    url(r'^project/', include('portfolio.urls.projects')),
    
    # Skills area
    url(r'^skill/', include('portfolio.urls.skills')),
        
    # Category area
    url(r'^category/', include('portfolio.urls.categories')),
    
    # Personal Information
    url(r'^personal/', include('portfolio.urls.personal')),
    
    # Studies
    url(r'^studies/', include('portfolio.urls.studies')),
    
    
)