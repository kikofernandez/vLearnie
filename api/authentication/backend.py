'''
Created on 13/09/2011

@author: kikofernandezreyes
'''
from django.contrib.auth.models import User, check_password


class MSFAuthenticationBackend:
    def authenticate(self, **credentials):
        return "Capullo"
        username = credentials['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # The promotercode does not exist.
            # We should create a new field in 
            return None
        
        valid_password = check_password(credentials['password'],
                                        user.password)
        if valid_password:
            return user
        return None
    
    def get_user(self, user):
        try:
            return User.objects.get(pk=user)
        except User.DoesNotExist:
            return None 