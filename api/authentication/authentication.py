'''
Created on 13/09/2011

@author: kikofernandezreyes
'''
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponse
#from api.authentication.backend import PromoterAuthenticationBackend
from django.contrib.auth import authenticate

class HttpMSFAuthentication(object):
    """
    Basic HTTP authenticater. Synopsis:
    
    Authentication handlers must implement two methods:
     - `is_authenticated`: Will be called when checking for
        authentication. Receives a `request` object, please
        set your `User` object on `request.user`, otherwise
        return False (or something that evaluates to False.)
     - `challenge`: In cases where `is_authenticated` returns
        False, the result of this method will be returned.
        This will usually be a `HttpResponse` object with
        some kind of challenge headers and 401 code on it.
    """
    def __init__(self, auth_func=authenticate, realm='My sample API'):
        self.auth_func = auth_func
        self.realm = realm

    def is_authenticated(self, request):
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)
        
        print request
        
        if not auth_string:
            return False
            
        (authmeth, auth) = auth_string.split(" ", 1)
        
        print auth
        if not authmeth.lower() == 'basic':
            return False
        
        auth = auth.strip().decode('base64')
        print auth.split(':')
        (database, username, password) = auth.split(':')
        #return "%s, %s" % (username, password)
        
        request.user = self.auth_func(username=username, password=password, database=database) \
            or AnonymousUser()
        
        return not request.user in (False, None, AnonymousUser())
        
    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        resp.status_code = 401
        return resp