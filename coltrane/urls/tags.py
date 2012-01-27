#from django.conf.urls.defaults import *
#from tagging.models import Tag
#from coltrane.models import Entry, Link
#
#urlpatterns = patterns('',
#    (r'^$',
#     'django.views.generic.list_detail.object_list',
#     {'queryset': Tag.objects.all(),},
#      #'cloud' : Tag.objects.cloud_for_model(Entry),},
#     'coltrane_tag_list'),
#    (r'^entries/(?P<tag>[\w-]+)/$',
#     'tagging.views.tagged_object_list',
#     {'queryset_or_model': Entry.live.all(),
#      'related_tags': False,
#      'template_name': 'coltrane/entries_by_tag.html'},
#     'coltrane_entries_tagged'),
#    (r'^links/(?P<tag>[\w-]+)/$',
#     'tagging.views.tagged_object_list',
#     {'queryset_or_model': Link,
#      'template_name': 'coltrane/links_by_tags.html'},
#     'coltrane_links_tagged'),
#)
