from django.contrib import admin
from django.contrib.contenttypes import generic
from community.models import Community, Resource #EntryCommunityResource, URLCommunityResource

class CommunityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}
    list_display = ['title',]

admin.site.register(Community, CommunityAdmin)

class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title'],}

admin.site.register(Resource, ResourceAdmin)    
    
#class EntryCommunityResourceAdmin(admin.ModelAdmin):
#    prepopulated_fields = {'slug':['title']}
#
#admin.site.register(EntryCommunityResource, EntryCommunityResourceAdmin)
#
#class URLCommunityResourceAdmin(admin.ModelAdmin):
#    prepopulated_fields = {'slug':['title']}

#admin.site.register(URLCommunityResource, EntryCommunityResourceAdmin)