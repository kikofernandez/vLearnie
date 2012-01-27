from community.models import Community, Resource #, EntryCommunityResource
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.date_based import archive_index, archive_year, archive_month, archive_day
from django.shortcuts import Http404, render_to_response, get_object_or_404
from django.contrib.auth import decorators
from django.template.context import RequestContext

MONTH = '01' 
DAY= "01"

def list_communities_public(request):
    return object_list(request,
                       queryset=Community.objects.all(),
                       paginate_by=10,
                       #page,
                       template_name='community/community_list.html',
                       #extra_context,
                       )

def search(request, template="community/search.html"):
    data = request.POST
    print data
    if data.get('value'):
        value = data['value'].lower()
        if value is None:
            community = None
        else:
            community = Community.objects.filter(title__icontains=value)
    else:
        community = Community.objects.all()
    return render_to_response(template,
                              {'community': community},
                              context_instance=RequestContext(request))

def community_index(request):
    """
    Returns a list with all the communities
    
    **Arguments:**
        * ``request``
    
    **Template:**
    ``community/main_index.html``
    
    **Decorators:**
        :func:`django.contrib.auth.decorators.login_required`
        
    **Context-variables:**
        * communities: list with the created communities
    """
    
    communities = Community.objects.select_related().all()
    return render_to_response('community/community_admin_main_index.html',
                              {'communities': communities}, 
                              context_instance=RequestContext(request))
community_index = decorators.login_required(community_index)



def resume_index(request, community):
    """
    Returns to the index of that community
    
    **Arguments:**
        * ``request``
        * community: community to watch
    
    **Template:**
    ``community/archive_index.html``
    
        
    **Context-variables:**
        * community: the community object
        * resources: list with the resources of the community (entries + urls)
    
    **Raise:**
        :class:`django.http.Http404` if no :class:`Community <community.models.Community>`
        object exist. 
    """
    c = get_object_or_404(Community, slug=community)
    return render_to_response('community/archive_index.html',
                              {#'resources': c.resource_set.all().order_by('-pub_date'),
                               'resources': Community.objects.live_resources(c).order_by('-pub_date'),
                               'community': community},
                              RequestContext(request))
#    return archive_index(request,
#                         queryset=Community.objects.filter(slug=community),
#                         date_field,
#                         template_name='community/archive_index.html',
#                         extra_context)


def show_resources_by_year(request, community, year):
    """
    Returns to the index where you will see only the elements of the corresponding ``year``
    
    **Arguments:**
        * ``request``
        * ``community``: community to watch
        * ``year``
    
    **Template:**
    ``community/resource_archive_year.html``
    
    **Context-variables:**
        * community: the community object
    
    **Returns:**
        <archive_year `django.views.generic.date_based.archive_year`> view.
    
    **Raise:**
        :class:`django.http.Http404` if no :class:`Community <community.models.Community>`
        object exist. 
    """
    
    import time, datetime

    date_stamp = time.strptime(year+MONTH+DAY, "%Y%m%d")
    pubdate = datetime.date(*date_stamp[:3])
    c = get_object_or_404(Community, slug=community)
    query = Community.objects.live_resources(c)
    query = query.select_related(depth=2).filter(pub_date__year=pubdate.year)
#    query = c.resource_set.select_related(depth=2).filter(pub_date__year=pubdate.year)
    
    return archive_year(request,
                        year=year,
                        queryset = query.order_by('-pub_date'), 
                        date_field='pub_date',
                        template_name='community/resource_archive_year.html',
                        extra_context={'community':community},) 

def show_resources_by_month(request, community, year, month):
    """
    Returns to the index where you will see only the elements of the 
    corresponding ``year``, ``month``
    
    **Arguments:**
        * ``request``
        * ``community``: community to watch
        * ``year``
        * ``month``
    
    **Template:**
    ``community/resource_archive_month.html``
    
    **Context-variables:**
        * community: the community object
    
    **Returns:**
        <archive_month `django.views.generic.date_based.archive_month`> view.
    
    **Raise:**
        :class:`django.http.Http404` if no :class:`Community <community.models.Community>`
        object exist. 
    """
    
    import time, datetime

    date_stamp = time.strptime(year+month+DAY, "%Y%m%d")
    pubdate = datetime.date(*date_stamp[:3])
    c = get_object_or_404(Community, slug=community)
    query = Community.objects.live_resources(c)
    query = query.select_related(depth=2).filter(pub_date__year=pubdate.year,
                                                pub_date__month=pubdate.month)
#    query = c.resource_set.select_related(depth=2).filter(pub_date__year=pubdate.year,
#                                                          pub_date__month=pubdate.month)
    return archive_month(request,
                         year=year,
                         month=month,
                         queryset = query.order_by('-pub_date'),
                         date_field='pub_date',
                         month_format="%m",
                         template_name='community/resource_archive_month.html',
                         extra_context={'community':community,}
                         ,)

def show_resources_by_day(request, community, year, month, day):
    """
    Returns to the index where you will see only the elements of the 
    corresponding ``year``, ``month``, ``day``
    
    **Arguments:**
        * ``request``
        * ``community``: community to watch
        * ``year``
        * ``month``
        * ``day``
    
    **Template:**
    ``community/resource_archive_day.html``
    
    **Context-variables:**
        * community: the community object
    
    **Returns:**
        <archive_day `django.views.generic.date_based.archive_day`> view.
    
    **Raise:**
        :class:`django.http.Http404` if no :class:`Community <community.models.Community>`
        object exist. 
    """
    import time, datetime

    date_stamp = time.strptime(year+month+day, "%Y%m%d")
    pubdate = datetime.date(*date_stamp[:3])
    c = get_object_or_404(Community, slug=community)
#    query = c.resource_set.select_related(depth=2).filter(pub_date__year=pubdate.year)
#    query = query.filter(pub_date__month=pubdate.month).filter(pub_date__day=pubdate.day)
    query = Community.objects.live_resources(c).select_related(depth=2)
    query = query.filter(pub_date__year=pubdate.year,
                         pub_date__month=pubdate.month,
                         pub_date__day=pubdate.day)
    return archive_day(request,
                       year=year,
                       month=month,
                       day=day,
                       queryset = query.order_by('-pub_date'),
                       date_field='pub_date',
                       month_format='%m',
                       day_format='%d',
                       template_name='community/resource_archive_day.html',
                       extra_context={'community':community,})

def show_object_resource_details(request, community, year, month, day, slug):
    """
    Returns to the resource especified by ``year``, ``month``, ``day`` and ``slug``
    
    **Arguments:**
        * ``request``
        * ``community``: community to watch
        * ``year``
        * ``month``
        * ``day``
        * ``slug``
    
    **Template:**
    ``community/resourcedetail.html``
    
    **Context-variables:**
        * object: the community resource
    
    **Raise:**
        :class:`django.http.Http404` if no :class:`Resource <community.models.Resource>`
        object exist. 
    """
    
    import time, datetime

    date_stamp = time.strptime(year+month+day, "%Y%m%d")
    pubdate = datetime.date(*date_stamp[:3])
    resource = get_object_or_404(Resource, community__slug=community,
                                           pub_date__year = pubdate.year,
                                           pub_date__month = pubdate.month,
                                           pub_date__day = pubdate.day,
                                           slug = slug)
    return render_to_response('community/resource_detail.html',
                              {'object': resource,
                               'community': community},
                              RequestContext(request))