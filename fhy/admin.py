from django.contrib import admin
from fhy.models import *

class RootAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}

class FolderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}

class FileFHYAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}
    list_display = ['slug', 'object_id', 'space', 'content_type', 'file', 'pub_date']

class ImageFHYAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title'], 'file':['slug']}

admin.site.register(Root, RootAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(FileFHY, FileFHYAdmin)
admin.site.register(ImageFHY, ImageFHYAdmin)