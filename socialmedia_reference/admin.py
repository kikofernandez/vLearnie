from socialmedia_reference.models import SocialMediaReference
from django.contrib import admin

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['user', 'twitter', 'facebook', 'linkedin']

admin.site.register(SocialMediaReference, SocialMediaAdmin)
