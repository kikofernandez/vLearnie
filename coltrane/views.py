from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.date_based import archive_year, archive_month, archive_day
from coltrane.models import Category, Entry, Link
from space.models import Space
from tagging.models import Tag, TaggedItem
from tagging.views import tagged_object_list
from friendycontrol.decorator import show_if_permitted
from django.template.context import RequestContext
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User

LIVE_STATUS = 1
DRAFT_STATUS = 2
HIDDEN_STATUS = 3

#def category_list(request):
#    return render_to_response('coltrane/category_list.html',
#                              {'object_list': Category.objects.all()})

def search(request, template = 'coltrane/search.html'):
    data = request.POST
    if data.get('value'):
        type =  data['type'].lower()
        value = data['value'].lower()
        #print "%s, %s" % (type, value)
        if value is None:
            users = None
        elif type == 'username':
            users = User.objects.filter(username__istartswith = value)
        else:
            users = None
    else:
        users = None
    return render_to_response(template,
                              {'users': users},
                              context_instance=RequestContext(request))
    #return HttpResponse(simplejson.dumps(user.username))

def main_area(request):
    """
    This view returns an area where you can look for people spaces
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
    
    **Template:**
        * ``coltrane/main_area.html``
    
    **Decorators:**
        ``None``
    """
    return render_to_response('coltrane/main_area.html',
                              context_instance=RequestContext(request))
  
def category_list(request, username, spacename):
    """
    This view returns a list of categories. These categories are only shown
    if the entry to which they belong are marked as live. This view is used
    for people that want to read about the user categories.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * space_name: string containing the space_name to which belongs this file
    
    **Template:**
        * ``coltrane/category_list.html``
    
    **Decorators:**
        ``None``
    """
    entries = Entry.live.filter(author__username=request.user).filter(space__slug=spacename)
    l = []
    for en in entries:
        for category in en.categories.all():
            l.append(category)
    s = set(l)

    return render_to_response('coltrane/category_list.html',
                              {'object_list': s,
                               'number_categories': s.__len__(),
                               'username': username,
                               'spacename': spacename},
                               context_instance=RequestContext(request))

def category_detail(request, username, spacename, slug):
    """
    This view returns a detail view of the category selected. The category is only
    shown. This view is used for people that want to get knowledge of a specific
    category.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * space_name: string containing the space_name to which belongs this file
        * slug: string that contains the slug for the category
    
    **Template:**
        * ``coltrane/category_detail.html``
    
    **Decorators:**
        ``None``
    """
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('coltrane/category_detail.html',
                              {'object_list': category.live_entry_set(),
                               'category': category,
                               'username': username,
                               'spacename': spacename},
                               context_instance=RequestContext(request))

def show_spaces_by_username(request, username):
    """
    This view returns a list of spaces for the specific username.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
    
    **Template:**
        * ``coltrane/space_archive_by_username.html``
    
    **Decorators:**
        ``None``
    """
    return object_list(request, queryset=Space.objects.filter(user__username=username), 
                       template_name="coltrane/space_archive_by_username.html", 
                       extra_context={'username': username })

# copy from space.views.show_user_space.
# maybe we can pass a template_name as a variable so I can reuse this very same
# view function, but providing different content.
# Actually is not the same, but almost equal.
def show_content_by_space_username(request, username, spacename):
    """
    This view returns a list of spaces for the specific username.
    
    **Type:**
        * semi-public (requires permission of the user)
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
    
    **Template:**
        * ``coltrane/content_archive_by_space_username.html``
    
    **Decorators:**
        None
    """
#    space = get_object_or_404(Space, slug=spacename,
#                                     user__username=username)
    space = Space.objects.select_related().filter(slug=spacename).get(user__username=username)
        
    blog = space.entry_set.all().select_related(depth=2).filter(status=LIVE_STATUS)
    return object_list(request,
                       queryset=blog, 
                       template_name='coltrane/content_archive_by_space_username.html', 
                       extra_context = {'username': username,
                                        'spacename': spacename},
                       )
#show_content_by_space_username = show_if_permitted(show_content_by_space_username)

def show_entry_index(request, username, spacename):
    """
    This view returns to the index of the user space.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
    
    **Template:**
        * ``coltrane/entry_archive.html`` (via :func:`object_list <django.views.generic.list_detail.object_list>`)
    
    **Decorators:**
        None
    """
    return object_list(request,
                       queryset=Entry.live.filter(author__username=username).filter(space__slug=spacename),
                       template_name='coltrane/entry_archive.html',
                       extra_context={'username': username,
                                      'spacename': spacename },
                       #context_processors
                       )
show_entry_index = show_if_permitted(show_entry_index)
    
def show_entries_by_year(request, username, spacename, year):
    """
    This view returns a list of entries by year. This list only shows entries that
    have been marked as 'live'.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * year: integer for showing the entries in that year
    
    **Template:**
        * ``coltrane/entry_archive_year.html`` (via :func:`object_list <django.views.generic.date_based.archive_year>`)
    
    **Decorators:**
        None
    """
    
    import time, datetime
    MONTH = DAY= "1"
    date_stamp = time.strptime(year+MONTH+DAY, "%Y%m%d")
    date_year = datetime.date(*date_stamp[:3]) 
    entryset = Entry.live.filter(author__username=username).filter(space__slug=spacename).filter(pub_date__year=date_year.year)

    return archive_year(request,
                        year = year,
                        queryset=entryset,
                        date_field='pub_date',
                        template_name='coltrane/entry_archive_year.html',
                        extra_context={'username': username,
                                      'spacename': spacename },
                        )

    
def show_entries_by_month(request, username, spacename, year, month):
    """
    This view returns a list of entries by year and month. This list only shows entries that
    have been marked as 'live'.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * year: integer for showing the entries in that year
        * month: integer for showing the entries in that month
    
    **Template:**
        * ``coltrane/entry_archive_month.html`` (via :func:`object_list <django.views.generic.date_based.archive_month>`)
    
    **Decorators:**
        None
    """
    import time, datetime
    DAY= "1"
    date_stamp = time.strptime(year+month+DAY, "%Y%b%d")
    date_stamp = datetime.date(*date_stamp[:3]) 
    entryset = Entry.live.filter(author__username=username).filter(space__slug=spacename).filter(pub_date__year=date_stamp.year)
    entryset = entryset.filter(pub_date__month = date_stamp.month)
    
    return archive_month(request,
                        year = year,
                        month = month,
                        queryset=entryset,
                        date_field='pub_date',
                        template_name='coltrane/entry_archive_month.html',
                        extra_context={'username': username,
                                      'spacename': spacename,
                                      },
                        )

def show_entry_by_day(request, username, spacename, year, month, day):
    """
    This view returns a list of entries by year, month and day. This list only shows entries that
    have been marked as 'live'.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * year: integer for showing the entries in that year
        * month: integer for showing the entries in that month
        * day: integer for showing the entries in that day
    
    **Template:**
        * ``coltrane/entry_archive_day.html`` (via :func:`object_list <django.views.generic.date_based.archive_day>`)
    
    **Decorators:**
        None
    """
    import time, datetime
    date_stamp = time.strptime(year+month+day, "%Y%b%d")
    date_stamp = datetime.date(*date_stamp[:3]) 
    entryset = Entry.live.filter(author__username=username).filter(space__slug=spacename).filter(pub_date=date_stamp)
    
    
    return archive_day(request,
                       year = year,
                       month = month,
                       day = day,
                       queryset=entryset,
                       date_field='pub_date',
                       template_name='coltrane/entry_archive_day.html',
                       extra_context={'username': username,
                                      'spacename': spacename,
                                      },
                        )

def show_entry_details(request, username, spacename, year, month, day, slug):
    """
    This view gives you the entry. This list only shows entries that
    have been marked as 'live'.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * year: integer for showing the entries in that year
        * month: integer for showing the entries in that month
        * day: integer for showing the entries in that day
        * slug: string which is the slug of the entry
    
    **Template:**
        * ``coltrane/entry_detail.html``
    
    **Decorators:**
        None
    """
    import datetime, time
    date_stamp = time.strptime(year+month+day, "%Y%b%d")
    pub_date = datetime.date(*date_stamp[:3])
    entry = Entry.live.filter(author__username=username).filter(space__slug=spacename)
    entry = get_object_or_404(entry, pub_date__year = pub_date.year,
                                     pub_date__month = pub_date.month,
                                     pub_date__day = pub_date.day,
                                     slug = slug)
    return render_to_response('coltrane/entry_detail.html',
                              {'object': entry,
                               'username': username,
                               'spacename': spacename},
                               RequestContext(request))
    
    
## LINKS

def show_link_index(request, username, spacename):
    """
    This view gives you the link index where you have all your links.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
    
    **Template:**
        * ``coltrane/link_archive.html``
    
    **Decorators:**
        None
    """
    #print Link.objects.filter(posted_by__username=username).filter(space__slug=spacename)
    return object_list(request,
                       queryset=Link.objects.filter(posted_by__username=username).filter(space__slug=spacename),
                       template_name='coltrane/link_archive.html',
                       extra_context={'username': username,
                                      'spacename': spacename },
                       #context_processors
                       )
    
def show_links_by_year(request, username, spacename, year):
    """
    This view gives you the links by year.
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * year: integer for showing the links in that year
    
    **Template:**
        * ``coltrane/link_archive_year.html``
    
    **Decorators:**
        None
    """
    import time, datetime
    MONTH = DAY= "1"
    date_stamp = time.strptime(year+MONTH+DAY, "%Y%m%d")
    date_year = datetime.date(*date_stamp[:3]) 
    linkset = Link.objects.filter(posted_by__username=username).filter(space__slug=spacename).filter(pub_date__year=date_year.year)

    return archive_year(request,
                        year = year,
                        queryset=linkset,
                        date_field='pub_date',
                        template_name='coltrane/link_archive_year.html',
                        extra_context={'username': username,
                                      'spacename': spacename },)
    
def show_links_by_month(request, username, spacename, year, month):
    """
    This view gives you links by year and month
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * year: integer for showing the links in that year
        * month: integer for showing the links in that month

    
    **Template:**
        * ``coltrane/link_archive_month.html``
    
    **Decorators:**
        None
    """
    
    import time, datetime
    DAY= "1"
    date_stamp = time.strptime(year+month+DAY, "%Y%b%d")
    date_stamp = datetime.date(*date_stamp[:3]) 
    linkset = Link.objects.filter(posted_by__username=username).filter(space__slug=spacename).filter(pub_date__year=date_stamp.year)
    linkset = linkset.filter(pub_date__month = date_stamp.month)
    
    return archive_month(request,
                        year = year,
                        month = month,
                        queryset=linkset,
                        date_field='pub_date',
                        template_name='coltrane/link_archive_month.html',
                        extra_context={'username': username,
                                      'spacename': spacename,
                                      },)

def show_link_by_day(request, username, spacename, year, month, day):
    """
    This view gives you the links by year, month and day
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * year: integer for showing the entries in that year
        * month: integer for showing the entries in that month
        * day: integer for showing the entries in that day
    
    **Template:**
        * ``coltrane/link_archive_day.html``
    
    **Decorators:**
        None
    """
    
    import time, datetime
    date_stamp = time.strptime(year+month+day, "%Y%b%d")
    date_stamp = datetime.date(*date_stamp[:3]) 
    linkset = Link.objects.filter(posted_by__username=username).filter(space__slug=spacename).filter(pub_date=date_stamp)
        
    return archive_day(request,
                       year = year,
                       month = month,
                       day = day,
                       queryset=linkset,
                       date_field='pub_date',
                       template_name='coltrane/link_archive_day.html',
                       extra_context={'username': username,
                                      'spacename': spacename,
                                      },)

def show_link_details(request, username, spacename, year, month, day, slug):
    """
    This view gives you the link details. 
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * year: integer for showing the links in that year
        * month: integer for showing the links in that month
        * day: integer for showing the links in that day
        * slug: string which is the slug of the link
    
    **Template:**
        * ``coltrane/link_detail.html``
    
    **Decorators:**
        None
    """
    
    import datetime, time
    date_stamp = time.strptime(year+month+day, "%Y%b%d")
    pub_date = datetime.date(*date_stamp[:3])
    link = Link.objects.filter(posted_by__username=username).filter(space__slug=spacename)
    link = get_object_or_404(link, pub_date__year = pub_date.year,
                                     pub_date__month = pub_date.month,
                                     pub_date__day = pub_date.day,
                                     slug = slug)
    return render_to_response('coltrane/link_detail.html',
                              {'object': link,
                               'username': username,
                               'spacename': spacename},
                               context_instance=RequestContext(request))    
    
def show_tag_index(request, username, spacename):
    """
    This view gives you the tags index. The tags are separated for entries and links
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
    
    **Template:**
        * ``coltrane/tags_by_space.html``
    
    **Decorators:**
        None
    """
    
    space = Space.objects.select_related(depth=2).filter(user__username=username).get(slug=spacename)
    entries = space.entry_set.filter(status = LIVE_STATUS)
    tag_list = Tag.objects.usage_for_queryset(queryset=entries)
    #tag_list = list()
    #link_list = []
    #for entry in entries:
    #    tag_list.extend(entry.tags.split())
    links = Link.objects.filter(posted_by__username=username).filter(space__slug=spacename)
    link_list = Tag.objects.usage_for_queryset(queryset=links)
    #for link in links:
    #    link_list.extend(link.tags.split())
    
    return render_to_response('coltrane/tags_by_space.html',
                             {'tags': set(tag_list),
                              'links': set(link_list),
                              'username': username,
                              'spacename': spacename},
                              context_instance=RequestContext(request))

def show_tagged_object_list(request, username, spacename, tag):
    """
    This view gives you the entries that have been marked with the ``tag``
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * tag: tag to consult
    
    **Template:**
        * ``coltrane/entries_by_tag.html``
    
    **Decorators:**
        None
    """
    e = Entry.live.filter(space__slug=spacename).filter(author__username=username)
    tags = Tag.objects.select_related(depth=2).get(id=tag)
    
    # This comment want to leave because I have changed the template that it
    # renders, plus the url config file, so leave for now.
    #e.filter(tags__icontains=tag)
    
    return tagged_object_list(request, 
                              queryset_or_model=e.filter(tags__icontains=tags.name),
                                                # idem
                                                #e.filter(tags__icontains=tag), 
                              tag = tags.name,
                              related_tags=False,
                              template_name = 'coltrane/entries_by_tag.html',
                              extra_context={'username': username,
                                             'spacename': spacename,
                                             'tags': e.filter(tags__icontains=tags.name), 
                                                    # idem
                                                    #e.filter(tags__icontains=tag),
                                            },)

def show_tagged_links_object_list(request, username, spacename, tag):
    """
    This view gives you the links that have been marked with the ``tag``
    
    **Type:**
        * public
    
    **Arguments:** 
        * request: Request object
        * username: string containing the username
        * spacename: name of the space that you want to watch
        * tag: tag to consult
    
    **Template:**
        * ``coltrane/entry_detail.html``
    
    **Decorators:**
        None
    """
    
    l = Link.objects.filter(posted_by__username=username).filter(space__slug=spacename)
    #l.filter(tags__icontains=tag)
    tags = Tag.objects.select_related(depth=2).get(id=tag)
    return tagged_object_list(request, 
                              #queryset_or_model=l.filter(tags__icontains=tag),
                              queryset_or_model=l.filter(tags__icontains=tags.name),
                              tag = tags.name,
                              related_tags = False,
                              template_name='coltrane/links_by_tags.html',
                              extra_context={'username': username,
                                             'spacename': spacename,
                                            })

show_entries_by_year = show_if_permitted(show_entries_by_year)
show_entries_by_month = show_if_permitted(show_entries_by_month)
show_entry_by_day = show_if_permitted(show_entry_by_day)
show_entry_details = show_if_permitted(show_entry_details)

show_links_by_year = show_if_permitted(show_links_by_year)
show_links_by_month = show_if_permitted(show_links_by_month)
show_link_by_day = show_if_permitted(show_link_by_day)
show_link_details = show_if_permitted(show_link_details)

show_tag_index = show_if_permitted(show_tag_index)
show_tagged_object_list = show_if_permitted(show_tagged_object_list)
show_tagged_links_object_list = show_if_permitted(show_tagged_links_object_list)

category_list = show_if_permitted(category_list)
category_detail = show_if_permitted(category_detail)