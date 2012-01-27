'''
Created on 13/10/2011

@author: kikofernandezreyes
'''
from community.models import Community, Resource
from django.http import Http404
from django.shortcuts import get_object_or_404
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc
from portfolio.models import PersonalInformation, Study, Project, Skill,\
    Category
from django.template.defaultfilters import slugify
#from coltrane.models import *

NOT_ALLOWED = 'You are not allowed to do this action'
MANDATORY_PARAMETER_MISSING = 'There are mantatory paramenters that are missing'

class AnonymousPortfolioHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)
    model = PersonalInformation
    fields = ('bio_html', 'first_name', 'last_name', 'birthday', 
              ('user',('username', 'first_name', 'last_name', 'id')))
#    def read(self, request, id=None):
#        base = PersonalInformation.objects
#        
#        if id is None:
#            return base.all();
#        else:
#            return base.get(id=id)

class PortfolioHandler(BaseHandler):
    allowed_methods = ("GET", "POST", 'PUT', 'DELETE')
    anonymous = AnonymousPortfolioHandler
    fields = ('bio_html', 'first_name', 'last_name', 'birthday', 
              ('user',('username', 'first_name', 'last_name', 'id')),'id')
    model = PersonalInformation
    
    def create(self, request):
        try:
            p = PersonalInformation.objects.get(user=request.user)
            return p
        except PersonalInformation.DoesNotExist:
            pass
        attrs = self.flatten_dict(request.POST)
        user = request.user
        try:
            first_name = attrs['first_name']
            last_name = attrs['last_name']
        except KeyError:
            return MANDATORY_PARAMETER_MISSING
        birthday = attrs.get('birthday')
        current_address = attrs.get('current_address')
        bio = attrs.get('bio')
        p = PersonalInformation(user=user,
                                first_name=first_name,
                                last_name=last_name,
                                birthday='' if birthday is None else birthday,
                                current_address='' if current_address is None else current_address,
                                bio='' if bio is None else bio)
        p.save()
        return p
    
    def update(self, request, id):
        pers = PersonalInformation.objects.get(pk=id)
        if pers.user == request.user:
            attrs = self.flatten_dict(request.PUT)
            first_name = attrs.get('first_name')
            if first_name is not None:
                pers.first_name = first_name
                
            last_name = attrs.get('last_name')
            if last_name is not None:
                pers.last_name = last_name
                
            birthday = attrs.get('birthday')
            if birthday is not None:
                pers.birthday = birthday
            
            current_address = attrs.get('current_address')
            if current_address is not None:
                pers.current_address = current_address
            
            bio = attrs.get('bio')
            if bio is not None:
                pers.bio = bio
            
            return rc.ALL_OK
    
    def delete(self, request, id):
        pers = PersonalInformation.objects.get(pk=id)
        if pers.user == request.user:
            pers.delete()
            return rc.DELETED

class AnonymousStudyHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)
    model = Study
    fields = ('end', 'speciality', 'title', 'additional_info', 'start',
              'place', 'user_id', 'id')
    
    def read(self, request, id=None):
        base = Study.objects
        
        if id is None:
            return base.all()
        else:
            return base.filter(user__id=id)

class StudyHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    anonymous = AnonymousStudyHandler
    model = Study
    fields = ('end', 'speciality', 'title', 'additional_info', 'start',
              'place', 'user_id', 'id')
    
    def read(self, request, id=None, user=None):
        if user is not None:
            return Study.objects.filter(user__username=user)
        elif id is not None:
            return Study.objects.filter(user__id=id)
        else:
            return Study.objects.all()
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            place = attrs['place']
            title = attrs['title']
            start = attrs['start']
        except KeyError:
            return "It's mandatory the place, title and start date in format YYYY-MM-DD"
        
        end = attrs.get('end')
        speciality = attrs.get('speciality')
        additional_info = attrs.get('additional_info')
        study = Study(user=request.user,
                      place = place,
                      title = title,
                      start = start,
                      end = end,
                      speciality = "" if speciality is None else speciality,
                      additional_info = "" if additional_info is None else additional_info)
        study.save()
        return study
    
    def update(self, request, id):
        study = Study.objects.get(pk=id)
        if study.user == request.user:
            attrs = self.flatten_dict(request.PUT)
            place = attrs.get('place')
            if place is not None:
                study.place = place
                
            title = attrs.get('title')
            if title is not None:
                study.title = title
                
            start = attrs.get('start')
            if start is not None:
                study.start = start
                
            end = attrs.get('end')
            if end is not None:
                study.end = end
                
            speciality = attrs.get('speciality')
            if speciality is not None:
                study.speciality = speciality
                
            additional_info = attrs.get('additional_info')
            if additional_info is not None:
                study.additional_info = additional_info
            
            study.save()
            return study
        else: return "You are not allowed to change someone's study information"
    
    def delete(self, request, id):
        study = Study.objects.get(pk=id)
        if study.user == request.user:
            study.delete()
            return True
        else:
            return "You are not allowed to do this operation"

class AnonymousProjectHandler(AnonymousBaseHandler):
    """
    If an argument is passed, it will consider that argument
    as the id of the user.
    """
    allowed_method = ('GET',)
    fields = ("end_date","name", "description", "url", "start_date", "id", 
        "short_description", "pull_quote", "user_id", "category_id", "slug", )
    
    def read(self, request, id=None):
        base = Project.objects
        
        if id is None:
            return base.all()
        else:
            return base.filter(user__id=id)

class ProjectHandler(BaseHandler):
    allowed_method = ('GET', 'POST', 'PUT', 'DELETE')
    anonymous = AnonymousProjectHandler
    model = Project
    fields = (('user',('username', 'first_name', 'last_name', 'id')),
              ('category', (('user', ('username', 'first_name', 'last_name', 'id')), 'name', 'id')),
              'end_date', 'name', 'description', 'url', 'start_date',
              'pull_quote', 'short_description',
              'slug', 'description', 'id')
    
    def read(self, request, id=None, user=None):
        if id is not None:
            return Project.objects.filter(pk=id)
        elif user is not None:
            return Project.objects.filter(user__username=user)
        else:
            return Project.objects.all()
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            name = attrs['name']
            slug = slugify(name)
            category = Category.objects.get(attrs['category'])
            
        except KeyError:
            return MANDATORY_PARAMETER_MISSING
        except Category.DoesNotExist:
            return MANDATORY_PARAMETER_MISSING
        
        url = attrs.get('url')
        pull_quote = attrs.get('pull_quote')
        short_description = attrs.get('short_description')
        description = attrs.get('description')
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        user = request.user
#        skills = models.ManyToManyField('Skill')
        project = Project(name=name, slug=slug, category=category,
                            url="" if url is None else url,
                            pull_quote="" if pull_quote is None else pull_quote,
                            short_description="" if short_description is None else short_description,
                            description="" if description is None else description,
                            start_date= start_date,
                            end_date= end_date,
                            user=user)
        project.save()
        return project
    
    def update(self, request, id):
        project = Project.objects.get(pk=id)
        attrs = self.flatten_dict(request.PUT)
        if project.user == request.user:
            name = attrs.get('name')
            if name is not None:
                project.name = name
                project.slug = slugify(name)
            
            category = attrs.get('category')
            if category is not None:
                try:
                    cat_obj = Category.objects.get(pk=category)
                except Category.DoesNotExist:
                    return NOT_ALLOWED
                else:
                    project.category = cat_obj
            
            url= attrs.get('url')
            if url is not None:
                project.url = url
                
            pull_quote= attrs.get('pull_quote')
            if pull_quote is not None:
                project.pull_quote = pull_quote
                
            short_description= attrs.get('short_description')
            if short_description is not None:
                project.short_description = short_description
                
            description= attrs.get('description')
            if description is not None:
                project.description = description
                
            start_date= attrs.get('start_date')
            if start_date is not None:
                project.start_date = start_date
                
            end_date= attrs.get('end_date')
            if end_date is not None:
                project.end_date = end_date
            
            project.save()
            return project
        return NOT_ALLOWED
    
    def delete(self, request, id):
        user = request.user
        project = Project.objects.get(pk=id)
        if project.user == user:
            project.delete()
            return ""
        return NOT_ALLOWED
        
    
class AnonymousSkillHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)
    fields = ('name', ('user',('username', 'first_name', 'last_name', 'id')))
    model = Skill

class SkillHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Skill
    anonymous = AnonymousSkillHandler
    fields = ('name', ('user',('username', 'first_name', 'last_name', 'id')),
              'id')
    
    def read(self, request, id=None, user=None):
        if id is not None:
            return Skill.objects.filter(user__id=id)
        elif user is not None:
            return Skill.objects.filter(user__username=user)
        else:
            return Skill.objects.all()
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            name = attrs['name']
            slug = slugify(name)
            user = request.user
        except KeyError:
            return "You must set all the parameters"
        skill = Skill(name=name, slug=slug, user=user)
        skill.save()
        return skill
    
    def update(self, request, id):
        skill = Skill.objects.get(pk=id)
        attrs = self.flatten_dict(request.PUT)
        if skill.user == request.user:
            name = attrs.get('name')
            if name is not None:
                skill.name = name
                skill.slug = slugify(name)
            skill.save()
            return skill
            
    
    def delete(self, request, id):
        skill = Skill.objects.get(pk=id)
        if skill.user == request.user:
            skill.delete()
            return ""
        else:
            return NOT_ALLOWED
    
class AnonymousCategoryHandler(AnonymousBaseHandler):
    model = Category
    allowed_methods = ('GET',)
    fields = ('name',('user',('username', 'first_name', 'last_name', 'id')))

class CategoryHandler(BaseHandler):
    model = Category
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    anonymous = AnonymousCategoryHandler
    fields = ('name',('user',('username', 'first_name', 'last_name', 'id')),
              'id')
    
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        try:
            name = attrs['name']
            slug = slugify(name)
            position = attrs['position']
        except KeyError:
            return MANDATORY_PARAMETER_MISSING
        cat = Category(name=name, slug=slug, position=position, user=request.user)
        cat.save()
        return cat

    def update(self, request, id):
        cat = Category.objects.get(pk=id)
        attrs = self.flatten_dict(request.PUT)
        if cat.user == request.user:
            name = attrs.get('name')
            if name is not None:
                cat.name = name
                cat.slug = slugify(name)
            
            position = attrs.get('position')
            if position is not None:
                cat.position = position
            
            cat.save()
            return cat
    
    def delete(self, request, id):
        cat = Category.objects.get(pk=id)
        if cat.user == request.user:
            cat.delete()
            return ""
        return NOT_ALLOWED