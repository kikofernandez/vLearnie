from django.conf.urls.defaults import *
#from coltrane.models import Entry

#entry_info_dict = {'queryset' : Entry.live.all(),'date_field' : 'pub_date',}

urlpatterns = patterns('',
#    url(r'^(?P<username>[-\w]+)/(?P<spacename>[-\w]+)/blog/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
#     'coltrane.views.show_entry_details',
#     name='coltrane_entry_detail'),
    url(r'^$',
     'coltrane.views.show_link_index',
     name='coltrane_link_archive_index'),
    
    url(r'^(?P<year>\d{4})/$',
     'coltrane.views.show_links_by_year',
     name='coltrane_link_archive_year'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
     'coltrane.views.show_links_by_month',
     name='coltrane_link_archive_month'), 
     
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
     'coltrane.views.show_link_by_day',
     name='coltrane_link_archive_month'),
     
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
     'coltrane.views.show_link_details',
     name='coltrane_link_detail'),
)