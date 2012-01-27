'''
Created on 24/11/2011

@author: kikofernandezreyes
'''
from django.conf import settings
from django.contrib.auth.models import User, check_password
import md5

SALT_FROM_CONFIG_PHP = 'v=~K)P`DY]3{2&wn i/>Nw[Xb'

class MD5Authentication(object):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            new_password = password + SALT_FROM_CONFIG_PHP
            secure_password = md5.new(new_password)
            if user.check_password(secure_password.hexdigest()):
                return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None