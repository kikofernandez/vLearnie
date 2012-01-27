'''
Created on 01/03/2011

@author: kikofernandezreyes
'''
from django.contrib.auth.models import User
from sqlalchemy import MetaData, Column
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, BIGINT, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from msf.settings import DATABASES
from session.sessionexception import InvalidSessionPassword

USER_INFORMATION_TABLE = 'mdl_user'
USER = DATABASES.get('moodle').get('USER')
PASSWORD = DATABASES.get('moodle').get('PASSWORD')
HOST = DATABASES.get('moodle').get('HOST')
DBNAME = DATABASES.get('moodle').get('NAME')
PORT = DATABASES.get('moodle').get('PORT')


Base = declarative_base()
class MoodleMDLUser(Base):
    __tablename__ = USER_INFORMATION_TABLE
    
    id = Column(BIGINT, primary_key=True)
    auth = Column(VARCHAR(20), nullable=False, default='manual')
    confirmed = Column(TINYINT(1), nullable=False, default=0)
    policyagreed = Column(TINYINT(1), nullable=False, default=0)
    deleted = Column(TINYINT(1), nullable=False, default=0)
    mnethostid = Column(BIGINT(10), nullable=False, default=0)
    username = Column(VARCHAR(100), nullable=False)
    password = Column(VARCHAR(32), nullable=False)
    idnumber = Column(VARCHAR(255), nullable=False)
    firstname = Column(VARCHAR(100), nullable=False)
    lastname = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=False)
    emailstop = Column(TINYINT(1), nullable=False, default=0)
    icq = Column(VARCHAR(15), nullable=False)
    skype = Column(VARCHAR(50), nullable=False)
    yahoo = Column(VARCHAR(50), nullable=False)
    aim = Column(VARCHAR(50), nullable=False)
    msn = Column(VARCHAR(50), nullable=False)
    phone1 = Column(VARCHAR(20), nullable=False)
    phone2 = Column(VARCHAR(20), nullable=False)
    institution = Column(VARCHAR(40), nullable=False)
    department = Column(VARCHAR(30), nullable=False)
    address = Column(VARCHAR(70), nullable=False)
    city = Column(VARCHAR(20), nullable=False)
    country = Column(VARCHAR(2), nullable=False)
    lang = Column(VARCHAR(30), nullable=False, default='en_utf8')
    theme = Column(VARCHAR(50), nullable=False)
    timezone = Column(VARCHAR(100), nullable=False, default=99)
    firstaccess = Column(BIGINT(10), nullable=False, default=0)
    lastaccess = Column(BIGINT(10), nullable=False, default=0)
    lastlogin = Column(BIGINT(10), nullable=False, default=0)
    currentlogin = Column(BIGINT(10), nullable=False, default=0)
    lastip = Column(VARCHAR(15), nullable=False)
    secret = Column(VARCHAR(15), nullable=False)
    picture = Column(TINYINT(1), nullable=False, default=0)
    url = Column(VARCHAR(255), nullable=False)
    description = Column(TEXT)
    mailformat = Column(TINYINT(1), nullable=False, default=1)
    maildigest = Column(TINYINT(1), nullable=False, default=0)
    maildisplay = Column(TINYINT(2), nullable=False, default=2)
    htmleditor = Column(TINYINT(1), nullable=False, default=1)
    ajax = Column(TINYINT(1), nullable=False, default=1)
    autosubscribe = Column(TINYINT(1), nullable=False, default=1)
    trackforums = Column(TINYINT(1), nullable=False, default=0)
    timemodified = Column(BIGINT(10), nullable=False, default=0)
    trustbitmask = Column(BIGINT(10), nullable=False, default=0)
    imagealt = Column(VARCHAR(255))
    screenreader = Column(TINYINT(1), nullable=False, default=0)
    
    def __init__(self, id, auth, confirmed, policyagreed, deleted, mnethostid, username,
                 password, idnumber, firstname, lastname, email, emailstop, icq, skype, yahoo,
                 aim, msn, phone1, phone2, institution, department, address, city, country,
                 lang, theme, timezone, firstaccess, lastaccess, lastlogin, currentlogin,
                 lastip, secret, picture, url, description, mainformat, maildigest, maildisplay,
                 htmleditor, ajax, autosubscribe, trackforums, timemodified, trustbitmask,
                 imagealt, screenreader):
        self.id = id
        self.auth = auth
        self.confirmed = confirmed
        self.policyagreed = policyagreed
        self.deleted = deleted
        self.mnethostid = mnethostid
        self.username = username
        self.password = password
        self.idnumber = idnumber
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.emailstop = emailstop
        self.icq = icq
        self.skype = skype
        self.yahoo = yahoo
        self.aim = aim
        self.msn = msn
        self.phone1 = phone1
        self.phone2 = phone2
        self.institution = institution
        self.department = department
        self.address = address
        self.city = city
        self.country = country
        self.lang = lang
        self.theme = theme
        self.timezone = timezone
        self.firstaccess = firstaccess
        self.lastaccess = lastaccess
        self.lastlogin = lastlogin
        self.currentlogin = currentlogin
        self.lastip = lastip
        self.secret = secret
        self.picture = picture
        self.url = url
        self.description = description 
        self.mainformat = mainformat
        self.maildigest = maildigest
        self.maildisplay = maildisplay
        self.htmleditor = htmleditor
        self.ajax = ajax
        self.autosubscribe = autosubscribe
        self.trackforums = trackforums
        self.timemodified = timemodified
        self.trustbitmask = trustbitmask
        self.imagealt = imagealt
        self.screenreader = screenreader
    
        

class MoodleSessionBackend:
    """
This is my own backend for the Moodle connection to Django. The methods that are 
mandatory are:

    - def authenticate(self, username, password)
    - def get_user(self, username)

although both can be called with other parameters. In this case, we are going to
look for the username and password accessing to the Moodle Database and getting
the attributes from the table defined in the constants USERNAME_DATABASE_ATTRIBUTE
and PASSWORD__DATABASE_ATTRIBUTE.
Note that the user created has no password, which means that it will be accesible only
through the sessions that come under Moodle. This was done
"""   
    def mysql_engine(self):
        #engine = "
        return create_engine("mysql+mysqldb://%s:%s@%s:%s/%s" % 
                             (USER, PASSWORD, HOST, PORT, DBNAME))
    
    def __check_username_and_password_on_moodle(self, username, password):    
        engine = self.mysql_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        userinfo = self.__get_user_info(session, username)
        return userinfo
        #username_valid = self.__check_username( session, username)
        #password_valid = self.__check_password(session, username, password)
        #return True if username_valid and password_valid else False

    def __get_user_info(self,session, username=None):
        if username is None:
            return None
        
        querydb = session.query(MoodleMDLUser).filter_by(username=username)
        return querydb[0] if querydb[0].username is not None and querydb.count() == 1 else None
        
    ##################################
    # These two methods could just return the object, so that I can query for
    # more parameters
    ##################################

    def __check_username(self, session, username=None):
        if username is None: 
            return None
        # Now, look at the table in USERNAME_DATABASE_ATTRIBUTE and get the username
        #Base = declarative_base()
        querydb = session.query(MoodleMDLUser).filter_by(username=username)
        print "Query count: %s" % querydb.count()
        return querydb[0].username if querydb[0].username is not None and querydb.count() == 1 else None 
    
    def __check_password(self, session, username=None, password=None):
        if password is None or username is None:
            return None
        
        # Now look for the password encrypted in the DB and also in the variable.
        # If both of them are equal, return true, otherwise, return false
        querydb = session.query(MoodleMDLUser).filter_by(username=username)
        return querydb[0].password if querydb[0].password is not None and querydb.count() == 1 else None

    #################################
    
    def __create_user_from_information(self, username, password_not_converted):
        """
        Create the username with its password in the django db. Create a username with
        the given username and a password converting the md5 password receive
        from the moodle session to a django password.
        
        This implies redundancy (user objects in moodle db and django db) but 
        we have instead flexibility to create new users using some django app
        created by others
        """
        u = User.objects.create(username=username) 
        u.set_password(password_not_converted)
        return u
    
    def authenticate(self, username=None, password=None):
        """
        authenticate is the method that will return a User object or None. We will
        return None when we have check whether the user exists in Moodle with the
        given username and password. If it fails, then return None. If it succeeds,
        then we must check whether the User exists in Django db. If this is not, 
        then create the User object.
        """
        
        # First, check that the user and password are valid in the moodle db
        valid = self.__check_username_and_password_on_moodle(username, password)
        
        if valid:
            try:
                valid_user = User.objects.get(username=valid.username)
                
                # if the user is not valid, DoesNotExist will be raised 
                # and catch by the except block
                valid = valid_user.check_password(valid.password)
               # print "PASSWORD: %s, %s" % (password, valid)
                
                if valid:
                    user = valid_user
                else: 
                    #print " NONE....."
                    raise InvalidSessionPassword()
                    #user = None
            except (User.DoesNotExist, InvalidSessionPassword) as err:
                if isinstance(err, User.DoesNotExist):
                    #user = User(username=username, password=password)
                    user = self.__create_user_from_information(valid.username, valid.password)
                    user.is_staff = True
                    user.is_superuser = True
                    user.first_name = valid.firstname
                    user.last_name = valid.lastname
                    user.email = valid.email
                    user.save()
                    print "user type1: %s" % type(user)
                elif isinstance(err, InvalidSessionPassword):
                    print "Error using the moodle password in the Django DB"
                    raise Exception("Irrecuperable error")
            else:
                return user
        return None
        
    def get_user(self, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

#SESSION_KEY = '_auth_user_id'
#BACKEND_SESSION_KEY = '_auth_user_backend'
#      
#def login(request, user):
#    """
#    Persist a user id and a backend in the request. This way a user doesn't
#    have to reauthenticate on every request.
#    """
#    import datetime
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
#            print "Flush"
#            raise Exception("Flush")
#            request.session.flush()
#    else:
#        request.session.cycle_key()
#        print "Cycle_key"
#        raise Exception("Cycle key")
#    request.session[SESSION_KEY] = user.id
#    request.session[BACKEND_SESSION_KEY] = user.backend
#    print "OK"
#    if hasattr(request, 'user'):
#        request.user = user
        