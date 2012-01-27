from django.shortcuts import get_object_or_404
try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps  # Python 2.4 fallback.

from django.utils.decorators import available_attrs
from django.utils.http import urlquote
from friendycontrol.models import CompositionList, FriendPerson, RelationModel
from django.http import Http404
from django.contrib.auth.models import AnonymousUser

def show_if_permitted(function=None):
    def decorator(funct):
        def _wrapped_view(request, *args, **kwargs):
            path = urlquote(request.get_full_path())
            user, space =  path.split('/')[2:4]
            try:
#                c = CompositionList.objects.select_related().filter(owner__username=user,
#                                                                    spaces__slug__contains=space)
                c = CompositionList.objects.filter(owner__username=user, 
                                                   spaces__slug__contains=space, 
                                                   composition_list__friendperson__friend__username=user,
                                                   readable__relationmodel__content_type__app_label='space',
                                                   readable__read=True).distinct()
                
                if request.user.is_anonymous():
                    raise Http404('You have no permissions')
                
                # get the friends of the user (the one we want to watch the blog)
#                friend = get_object_or_404(FriendPerson, friend=request.user,
#                                                         friend_of__username=user)
                
            except (CompositionList.DoesNotExist, FriendPerson.DoesNotExist, Http404):
                raise Http404("You have no permissions")
            
#            composition_list = []
#            for composition in c:
#                for composition_object in composition.composition_list.all():
#                    if composition_object in friend.group_list.all():
#                        composition_list.append(composition)
            
            # Since the foreignkey is unique, there will be just one element in the list
#            readable_list = [composition.readable_set.all()[0] for composition in composition_list]
#            for readable in readable_list:
#                for relation_model in readable.relationmodel_set.all():
#                    if relation_model.content_type.app_label=='space' and readable.read:
#                        return funct(request, *args, **kwargs)    
            # If the composition exists, it means that the user
            # has privileges for reading the entry in the space
            if c:
                return funct(request, *args, **kwargs)                
            raise Http404('You do not have sufficient privileges')
            
        return wraps(funct, assigned=available_attrs(funct))(_wrapped_view)
    if function is None:
        return decorator
    return decorator(function)