from api.portfolio.handlers import PortfolioHandler, StudyHandler,\
    ProjectHandler, SkillHandler, CategoryHandler
from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from api.csrfexempt import CsrfExemptResource

auth = HttpBasicAuthentication(realm="My sample API")
personalinformation_handler = CsrfExemptResource(PortfolioHandler, authentication = auth)
studies_handler = CsrfExemptResource(StudyHandler, authentication = auth)
project_handler = CsrfExemptResource(ProjectHandler, authentication = auth)
skill_handler = CsrfExemptResource(SkillHandler, authentication = auth)
category_handler = CsrfExemptResource(CategoryHandler, authentication = auth)

urlpatterns = patterns('',
    url(r'^pinformation/$',
        personalinformation_handler,
        {'emitter_format':'json'}),
    url(r'^pinformation/(?P<id>\d+)/$',
        personalinformation_handler,
        {'emitter_format':'json'}),
    url(r'^studies/$',
        studies_handler,
        {'emitter_format':'json'}),
    url(r'^studies/(?P<id>\d+)/$',
        studies_handler,
        {'emitter_format':'json'}),
    url(r'^studies/(?P<user>\w+)/$',
        studies_handler,
        {'emitter_format':'json'}),
    url(r'^project/$',
        project_handler,
        {'emitter_format':'json'}),
    url(r'^project/(?P<id>\d+)/$',
        project_handler,
        {'emitter_format':'json'}),
    url(r'^project/(?P<user>\w+)/$',
        project_handler,
        {'emitter_format':'json'}),
    url(r'^skill/$',
        skill_handler,
        {'emitter_format':'json'}),
    url(r'^skill/(?P<id>\d+)/$',
        skill_handler,
        {'emitter_format':'json'}),
    url(r'^skill/(?P<user>\w+)/$',
        skill_handler,
        {'emitter_format':'json'}),
    url(r'^category/',
        category_handler,
        {'emitter_format':'json'}),
    url(r'^category/(?P<id>\d+)/$',
        category_handler,
        {'emitter_format':'json'}),
    
    # Any format is allowed
    
    url(r'^pinformation/(?P<emitter_format>\w+)/$',
        personalinformation_handler),
        
    url(r'^pinformation/(?P<id>\d+)/(?P<emitter_format>\w+)/$',
        personalinformation_handler),
    
    url(r'^pinformation/(?P<user>\w+)/(?P<emitter_format>\w+)/$',
        personalinformation_handler),
        
    url(r'^studies/(?P<emitter_format>\w+)/$',
        studies_handler),
        
    url(r'^studies/(?P<id>\d+)/(?P<emitter_format>\w+)/$',
        studies_handler),
        
    url(r'^studies/(?P<user>\w+)/(?P<emitter_format>\w+)/$',
        studies_handler),
        
    url(r'^project/(?P<emitter_format>\w+)/$',
        project_handler),
        
    url(r'^project/(?P<id>\d+)/(?P<emitter_format>\w+)/$',
        project_handler),
    
    url(r'^project/(?P<user>\w+)/(?P<emitter_format>\w+)/$',
        project_handler),
        
    url(r'^skill/(?P<emitter_format>\w+)/$',
        skill_handler),
        
    url(r'^skill/(?P<id>\d+)/(?P<emitter_format>\w+)/$',
        skill_handler),
    
    url(r'^skill/(?P<user>\w+)/(?P<emitter_format>\w+)/$',
        skill_handler),
        
    url(r'^category/(?P<emitter_format>\w+)/$',
        category_handler),
        
    url(r'^category/(?P<id>\d+)/(?P<emitter_format>\w+)/$',
        category_handler),
)