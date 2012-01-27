from portfolio.models import *
from django.shortcuts import get_object_or_404, render_to_response, Http404
from django.template.context import RequestContext
from django.contrib.auth import decorators
from portfolio.forms import ProjectForm, SkillForm, CategoryForm,\
    PersonalInformationForm, StudyForm
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list
from django.db.models import Max
from socialmedia_reference.forms import SocialMediaForm
from socialmedia_reference.models import SocialMediaReference

def manage_project(request):
    bio = PersonalInformation.objects.get(user=request.user)
    return render_to_response('portfolio/manage_project.html',
                              {'bio':bio},
                               context_instance = RequestContext(request))
manage_project = decorators.login_required(manage_project)
    
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.user, data=request.POST)
        print form.is_valid()
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.user = request.user
            new_project.save()
            return HttpResponseRedirect(reverse('portfolio_manage_portfolio'))
        #else:
            # If fails, usually Django do not take into account the initialization
            # that you did in ProjectForm, so you must load again the view
            # and also load the data coming
            #form = ProjectForm(user=request.user, data=request.POST)
    else:
        #category = Category.objects.filter(user=request.user)
        #skill = Skill.objects.filter(user=request.user)
        #print skill
        #user = request.user
        #form = ProjectForm(category)
        form = ProjectForm(user=request.user)
    return render_to_response('portfolio/project_form.html',
                              {'form': form,
                               'add': True},
                              context_instance=RequestContext(request))
create_project = decorators.login_required(create_project)


def edit_project(request, id):
    project = get_object_or_404(Project, user=request.user, id=id)
    if request.method == 'POST':
        form = ProjectForm(request.user, instance=project, data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('portfolio_manage_portfolio'))
#        else:
#            form = ProjectForm(user=request.user,instance=project)
    else:
        #category = Category.objects.filter(user=request.user)
        #form = ProjectForm(category, instance=project)
        form = ProjectForm(user=request.user, instance=project)
    return render_to_response('portfolio/project_form.html',
                              {'form': form,
                               'add': False},
                              context_instance=RequestContext(request))
edit_project = decorators.login_required(edit_project)


def delete_project(request, id):
    project = get_object_or_404(Project, user=request.user, id=id)
    project.delete()
    return HttpResponseRedirect(reverse('portfolio_manage_portfolio'))
delete_project = decorators.login_required(delete_project)

#############################
##
## SKill Area
##
############################

def skill_main(request):
    skill = Skill.objects.filter(user=request.user)
    bio = PersonalInformation.objects.get(user=request.user)
    return object_list(request,
                       queryset=skill,
                       template_name='portfolio/manage_skill.html', 
                       extra_context={'bio':bio},
                       )
skill_main = decorators.login_required(skill_main)

def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(data=request.POST)
        if form.is_valid():
            new_skill = form.save(commit=False)
            new_skill.user = request.user
            new_skill.save()
            return HttpResponseRedirect(reverse('portfolio_main_skill'))
            
    else:
        form = SkillForm()
    return render_to_response('portfolio/skill_form.html',
                              {'form': form,
                               'add':True},
                               context_instance=RequestContext(request))
create_skill = decorators.login_required(create_skill)


def edit_skill(request, id):
    skill = get_object_or_404(Skill, user=request.user, id=id)
    if request.method == 'POST':
        form = SkillForm(instance = skill, data=request.POST)
        form.save(commit=True)
        return HttpResponseRedirect(reverse('portfolio_main_skill'))
    else:
        form = SkillForm(instance=skill)
    return render_to_response('portfolio/skill_form.html',
                              {'form': form,
                               'add': False},
                               context_instance=RequestContext(request))
edit_skill = decorators.login_required(edit_skill)

def delete_skill(request, id):
    skill = get_object_or_404(Skill, user=request.user, id=id)
    skill.delete()
    return HttpResponseRedirect(reverse('portfolio_main_skill'))
delete_skill = decorators.login_required(delete_skill)


# Category area

def category_main(request):
    category = Category.objects.filter(user=request.user)
    bio = PersonalInformation.objects.filter(user=request.user)
    return object_list(request,
                       queryset=category,
                       template_name='portfolio/manage_category.html', 
                       extra_context={'bio':bio},
                       )
category_main = decorators.login_required(category_main)


def create_category(request):
    if request.method=='POST':
        form = CategoryForm(data=request.POST)
        
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.user = request.user
            max_number = Category.objects.filter(user=request.user).aggregate(Max('position'))['position__max']
            if max_number is None:
                max_number = 0
            new_category.position = max_number+1
            new_category.save()
            return HttpResponseRedirect(reverse('portfolio_main_category'))
    else:
        form = CategoryForm()
    return render_to_response('portfolio/category_form.html',
                              {'form':form,
                               'add': True},
                               context_instance=RequestContext(request))
create_category = decorators.login_required(create_category)


def edit_category(request, id):
    category = get_object_or_404(Category, user=request.user, id=id)
    if request.method == 'POST':
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('portfolio_main_category'))
    else:
        form = CategoryForm(instance=category)
    return render_to_response('portfolio/category_form.html',
                              {'form':form,
                               'add': False},
                               context_instance=RequestContext(request))
edit_category = decorators.login_required(edit_category)

def delete_category(request, id):
    category = get_object_or_404(Category, user=request.user, id=id)
    category.delete()
    return HttpResponseRedirect(reverse('portfolio_main_category'))
delete_category = decorators.login_required(delete_category)

# Personal Information

def personal_main(request):
    try:
        personal = PersonalInformation.objects.get(user=request.user)
    except PersonalInformation.DoesNotExist:
        personal = False
    try:
        social = SocialMediaReference.objects.get(user= request.user)
    except SocialMediaReference.DoesNotExist:
        social = False
    
    return render_to_response('portfolio/personal_info_main.html',
                                  {'user': request.user,
                                   'bio': personal,
                                   'social': social},
                                  context_instance=RequestContext(request))
personal_main = decorators.login_required(personal_main)

def create_personal(request):
    
    try:
        personal = get_object_or_404(PersonalInformation, user=request.user)
    except Http404:
        # You call create, and there are no other profile information,
        # so, let's create one
        if request.method == 'POST':
            form = PersonalInformationForm(data=request.POST)
            social_form = SocialMediaForm(data=request.POST)
            if form.is_valid() and social_form.is_valid():
                personal = form.save(commit=False)
                personal.user = request.user
                personal.save()
                
                social = social_form.save(commit=False)
                social.user = request.user
                social.save()
                return HttpResponseRedirect(reverse('portfolio_main_personal'))
        else:
            form = PersonalInformationForm()
            social_form = SocialMediaForm()
        return render_to_response('portfolio/personal_info_form.html',
                                  {'form': form,
                                   'social_form' : social_form,
                                   'add': True},
                                   context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('portfolio_edit_personal'))
create_personal = decorators.login_required(create_personal)

def edit_personal(request):
    personal = get_object_or_404(PersonalInformation, user=request.user)
    social = get_object_or_404(SocialMediaReference, user = request.user)
    if request.method == 'POST':
        form = PersonalInformationForm(instance=personal, data=request.POST)
        social_form = SocialMediaForm(instance=social, data=request.POST)
        
        if form.is_valid() and social_form.is_valid():
            form.save(commit=True)
            social_form.save(commit=True)
            return HttpResponseRedirect(reverse('portfolio_main_personal'))
    else:
        form = PersonalInformationForm(instance=personal)
        social_form = SocialMediaForm(instance=social)
    return render_to_response('portfolio/personal_info_form.html',
                              {'form': form,
                               'social_form': social_form,
                               'add': False},
                               context_instance=RequestContext(request))
edit_personal = decorators.login_required(edit_personal)

def delete_personal(request):
    PersonalInformation.objects.filter(user=request.user).delete()
    SocialMediaReference.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(reverse('portfolio_main_personal'))
delete_personal = decorators.login_required(delete_personal)

# STUDIES

def studies_main(request):
    return object_list(request,
                       queryset=Study.objects.filter(user=request.user).order_by('-end'),
                       template_name='portfolio/manage_studies.html',
                       extra_context = {
                            'bio': PersonalInformation.objects.filter(user=request.user),
                            },
                       )
studies_main = decorators.login_required(studies_main)

def create_studies(request):
    if request.method == 'POST':
        form = StudyForm(data=request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.user = request.user
            study.save()
            return HttpResponseRedirect(reverse('portfolio_main_studies'))
    else:
        form = StudyForm()
    return render_to_response('portfolio/studies_form.html',
                              {'form': form,
                               'add':True},
                              context_instance=RequestContext(request))
create_studies = decorators.login_required(create_studies)

def edit_studies(request, id):
    study = get_object_or_404(Study, user=request.user, id=id)
    
    if request.method == 'POST':
        form = StudyForm(instance=study, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('portfolio_main_studies'))
    else:
        form = StudyForm(instance=study)
    return render_to_response('portfolio/studies_form.html',
                              {'form': form,
                               'add':False},
                               context_instance=RequestContext(request))
edit_studies = decorators.login_required(edit_studies)

def delete_studies(request, id):
    Study.objects.filter(user=request.user, id=id).delete()
    return HttpResponseRedirect(reverse('portfolio_main_studies'))
delete_studies = decorators.login_required(delete_studies)