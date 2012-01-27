from friendycontrol.models import CompositionList, FriendListGroupName 
from friendycontrol.models import FriendPerson, Readable, RelationModel
from django.contrib import admin

class AdminCompositionList(admin.ModelAdmin):
    pass

class AdminFriendList(admin.ModelAdmin):
    pass

class AdminFriendPerson(admin.ModelAdmin):
    pass

class AdminReadable(admin.ModelAdmin):
    pass

class AdminRelationModel(admin.ModelAdmin):
    pass


admin.site.register(CompositionList, AdminCompositionList)
admin.site.register(FriendListGroupName, AdminFriendList)
admin.site.register(FriendPerson, AdminFriendPerson)
admin.site.register(Readable, AdminReadable)
admin.site.register(RelationModel, AdminRelationModel)