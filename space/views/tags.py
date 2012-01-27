from coltrane.models import Entry, Link
from space.models import Space
from tagging.models import Tag, TaggedItem
from django.shortcuts import render_to_response
from django.contrib.auth import decorators
from django.template.context import RequestContext

LIVE_STATUS = 1
DRAFT_STATUS = 2
HIDDEN_STATUS = 3


def show_user_tag(request, space_name):
    space = Space.objects.filter(user=request.user).get(slug=space_name)
    entries = space.entry_set.filter(status = LIVE_STATUS)
    tag_list = set()
    for entry in entries:
        tag_list.add(entry.tags)
    #print tag_list
    links = Link.objects.filter(posted_by__username=request.user).filter(space__slug=space_name)
    return render_to_response('space/tags_by_space.html',
                             {'tags': tag_list,
                              'user': request.user,
                              'space': space,
                              'links': links},
                             RequestContext(request))
show_user_tag = decorators.login_required(show_user_tag) 