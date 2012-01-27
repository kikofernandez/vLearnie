import time

#from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
#from django.contrib.sessions.models import Session
#from django.contrib.auth import models
from session.handshake import SessionStore
#from django.contrib.auth.models import User
from django.contrib.auth import login, logout
#from session.backend import login as nuevo_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
#from django.contrib.sites.models import Site
from msf.settings import LOGIN_URL

#from django.core.context_processors import csrf

from django.contrib.auth import SESSION_KEY
from msf.settings import MINUTES_ACTIVE_SESSION


#PATTERN = '(?<=username).+?.+?;.+?'

# Use this function if you want to read the username from the session_file
# Not recommended since the new version treat the file as an object.

#def get_session_username(s):
#    session_data = {}
#    try:
#        session_file = open(s._key_to_file(), "rb")
#        try:
#            file_data = session_file.read()
#            import re
#            m = re.search(PATTERN, file_data)
#            # This will return something like this:
#            # ['', 's:6:', '<username>', ';']
#            # We want the username, so that's why we take the [-2]
#            username = re.split('\"', m.group())[-2]
#            session_data['username'] = username
#        finally:
#            session_file.close()
#    except IOError:
#        pass
#    return session_data

#SESSION_KEY = '_auth_user_id'
#BACKEND_SESSION_KEY = '_auth_user_backend'
#REDIRECT_FIELD_NAME = 'next'
#import datetime

#def login(request, user):
#    if user is None:
#        user = request.user
#    # TODO: It would be nice to support different login methods, like signed cookies.
#    user.last_login = datetime.datetime.now()
#    user.save()
#
#    if SESSION_KEY in request.session:
#        if request.session[SESSION_KEY] != user.id:
#            # To avoid reusing another user's session, create a new, empty
#            # session if the existing session corresponds to a different
#            # authenticated user.
#            request.session.flush()
#    else:
#        #request.session.cycle_key()
#        print request.session_data
#    request.session[SESSION_KEY] = user.id
#    request.session[BACKEND_SESSION_KEY] = user.backend
#    if hasattr(request, 'user'):
#        request.user = user

def getsessionid(request):
    if request is None or 'MoodleSession' not in request.COOKIES:
        raise Http404
    
    if request.COOKIES['MoodleSession'] != None:
        sessionid = request.COOKIES['MoodleSession'] 

        s = SessionStore(session_key=sessionid)
        #print "Request cookies: %s" % request.COOKIES
        
        if ('username' or 'password' or 'lastaccess') not in s.get('USER').param:
            # We should redirect to the login page since the session has expired
            # or call an Http object telling that the session has expired
            #print "Accessed"
            #print Site.objects.get_current().name
            raise Http404
        elif int(s.get('USER').param.get('lastaccess'))+MINUTES_ACTIVE_SESSION < time.time():
            # check whether the session timeout was reached. This may happen
            # if the user does not closed the session through the logout link
            expired = str(int(s.get('USER').param.get('lastaccess'))+MINUTES_ACTIVE_SESSION)
            print "Last access: %s, time: %s" %  (expired, time.time())
            raise Exception("The session has timeout")  
        else:
            username = s.get('USER').param.get('username')
            password = s.get('USER').param.get('password')
            au = authenticate(username=username, password=password)
            # If this fails, it will be due to the user has changed the password,
            # meaning that we must update here the user password. There's no way
            # this could mean the user has entered the wrong password because
            # Moodle authenticates the user before redirecting to vLearnie.
            
            # We will do sth similar to this.
            #user = User.objects.get(username=username)
            #user.set_password(password)



        #print "request.session: %s" % 'True' if '_auth_user_id' in request.session else 'False'
        #request.session[SESSION_KEY] = au.id
        #print "Id: %s, request.session[Session_key]: %s " % (au.id, request.session[SESSION_KEY])
        #request.session = s

        # By doing this second authentication is when the session is really saved.
        # Dont ask me why, I'm still struggling my brains to find it out
        au = authenticate(username=username, password=password)
        #print "type(request.session): %s and type(s): %s" % (type(request.session), type(s))
        #request.session[SESSION_KEY] = int(au.id)
        #print "Id: %s, request.session[Session_key]: %s " % (au.id, request.session[SESSION_KEY])
        request.session['USER'].param['lastaccess'] = int(time.time())
        #print "Request.session USER param lastaccess: %s" % request.session['USER'].param['lastaccess']
        #print "Request.session[sesskey] = %s, userid=%s" % (request.session[SESSION_KEY], au.id)
        login(request, au)


        
        print request.COOKIES
        print "SESSION STORE:" 
        for k in request.session.keys():
            print "session_key: %s" % k 
        #request.COOKIES['MoodleSession'] = sessionid
        #h = HttpResponse()
        #print "Sessionid: %s" % (request.COOKIES.get('sessionid'))
        #print "MoodleSession: %s" %request.COOKIES.get('MoodleSession')
        #h.set_cookie(key='MoodleSession', value=request.COOKIES.get('sessionid'),  path='/')
        #return h
        #return HttpResponseRedirect("/profile/account/")
        #print request.GET.get('next')
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            #return HttpResponseRedirect(reverse('session_profile'))
            return HttpResponseRedirect(reverse('space_space_list_spaces'))
    else:
        print "nothing happens"
    raise Http404

def redirect_to_login_moodle(request):
    if request.COOKIES['MoodleSession'] != None:
        sessionid = request.COOKIES['MoodleSession'] 
        s = SessionStore(session_key=sessionid)
        request.session['USER'].param['lastaccess'] = int(time.time())
    
    return HttpResponseRedirect(LOGIN_URL)

def logout_request(request):
    logout(request)
    return HttpResponseRedirect(LOGIN_URL)