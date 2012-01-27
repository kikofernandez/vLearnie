from django.contrib import admin
from space.models import Space

class SpaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}

admin.site.register(Space, SpaceAdmin)