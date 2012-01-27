from django.views.generic.list_detail import object_detail, object_list
from portfolio.models import Project, Skill, Category, PersonalInformation,\
    Study
from django.shortcuts import get_object_or_404, Http404, render_to_response
from django.template.context import RequestContext

def project_context(username=None, category=None, slug=None):
    
    if username is None:
        categories = Category.objects.all()
        skills = Skill.objects.all()
    else:
        categories = Category.objects.filter(user__username=username)
        skills = Skill.objects.filter(user__username=username)
        bio = PersonalInformation.objects.filter(user__username = username)
        studies = Study.objects.filter(user__username = username).order_by('-end')
    return {
        'category_list': categories,
        'skill_list': skills,
        'username': username,
        'current_view': category,
        'current_slug': slug,
        'bio': bio,
        'studies': studies,
        }

def project_detail(request, username, slug,
                             template_name='portfolio/project_detail.html', extra_context={}):
    extra = project_context(username, 'project', slug)
    extra.update(extra_context)
    return object_detail(
        request,
        template_name = template_name,
        extra_context = extra,
        slug = slug,
        slug_field = 'slug',
        queryset = Project.objects.filter(user__username = username),
        )

def category_detail(request, username, slug,
                             template_name='portfolio/category_detail.html', extra_context={}):
    extra = project_context(username, 'category', slug)
    extra.update(extra_context)
    return object_detail(
        request,
        template_name = template_name,
        extra_context = extra,
        slug = slug,
        slug_field = 'slug',
        queryset = Category.objects.filter(user__username = username),
        )

def category_list(request,username,template_name='portfolio/category_list.html', extra_context={}):
    extra = project_context(username)
    extra.update(extra_context)
    return object_list(
        request,
        template_name = template_name,
        extra_context = extra,
        queryset = Category.objects.filter(user__username = username),
        )

def skill_detail(request, username, slug,
                            template_name='portfolio/skill_detail.html', extra_context={}):
    extra = project_context(username, 'skill', slug)
    extra.update(extra_context)
    return object_detail(
        request,
        template_name = template_name,
        extra_context = extra,
        slug = slug,
        slug_field = 'slug',
        queryset = Skill.objects.filter(user__username = username),
        )

def bio_detail(request, username, 
                        template_name='portfolio/bio_detail.html', extra_context={}):
    extra = project_context(username, 'bio')
    extra.update(extra_context)
    
    return render_to_response(template_name,
                              extra,
                              context_instance=RequestContext(request))
