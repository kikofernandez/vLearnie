from django.db import models
from django.contrib.auth.models import User
from markdown import markdown

class PersonalInformation(models.Model):
    """
    This represents the public information of the user.
    
    **Arguments:**
        id: Autofield
        user: ForeignKey(User)
        first_name: Your first name
        last_name: Your last name
        birthday: Birthday, optional field
        current_address: Address, optional field
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    birthday = models.DateField(blank=True,
                                help_text='Optional.')
    current_address = models.TextField(blank=True,
                                       help_text='Optional.')
    bio = models.TextField(blank=True,
                           help_text='Optional.')
    bio_html = models.TextField(editable=False, blank=True)
    
    class Meta:
        ordering = ['-first_name', 'last_name']
    
    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)
    
    def save(self, force_insert=False, force_update=False):
        if self.bio:
            self.bio_html = markdown(self.bio)
        super(PersonalInformation, self).save(force_insert, force_update)
    
class Study(models.Model):
    """
    This represents the user's studies
    
    **Arguments:**
        person: Reference to PersonalInformation
        place: Where did you actually study 
        title: What title did you get
        start: Starting in
        end: Till (optional, because you may not have finished yet)
        speciality: Speciality of your studies
        additional_info: Anything to add?
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    place = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField(blank=True,
                           null=True,
                           help_text='Optional. You have not finished yet.')
    speciality = models.TextField(blank=True,
                                  help_text='Optional.')
    speciality_html = models.TextField(editable=False,
                                       blank=True)
    additional_info = models.TextField(blank=True,
                                       help_text='Optional')
    additional_info_html = models.TextField(editable=False,
                                            blank=True)
    
    class Meta:
        verbose_name_plural = 'Studies'
    
    def __unicode__(self):
        return "%s, %s" % (self.title, self.place)
    
    def save(self, force_insert=False, force_update=False):
        if self.speciality:
            self.speciality_html = markdown(self.speciality)
        if self.additional_info:
            self.additional_info_html = markdown(self.additional_info)
        super(Study, self).save(force_insert, force_update)

class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    url = models.URLField(blank=True, null=True)
    pull_quote = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True)
    short_description_html = models.TextField(blank=True,
                                              editable=False)
    description = models.TextField()
    description_html = models.TextField(blank=True, 
                                   editable=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    category = models.ForeignKey('Category')
    skills = models.ManyToManyField('Skill')
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['-start_date', '-end_date', ]

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False):
        self.description_html = markdown(self.description)
        if self.short_description:
            self.short_description_html = markdown(self.short_description)
        super(Project, self).save(force_insert, force_update)

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio.views.project_detail', (), {'slug': str(self.slug), })
    

class Skill(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio.views.skill_detail', (), {'slug': str(self.slug), })

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    position = models.PositiveIntegerField()
    user = models.ForeignKey(User, related_name='user_portfolio_set')

    class Meta:
        ordering = ["position"]
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio.views.category_detail', (), {'slug': str(self.slug), })

# The following are not used.
class ProjectFile(models.Model):
    project = models.ForeignKey('Project')
    file = models.FileField(upload_to="project_file/%Y/%m/%d")
    desc = models.TextField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.file.name

    def get_absolute_url(self):
        return self.file.url

class ProjectImage(models.Model):
    project = models.ForeignKey('Project')
    image = models.ImageField(upload_to="project_image/%Y/%m/%d")
    desc = models.TextField()
    user = models.ForeignKey(User) 

    def __unicode__(self):
        return self.image.name

    def get_absolute_url(self):
        return self.image.url
