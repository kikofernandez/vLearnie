from django.contrib.sessions.backends.file import SessionStore as SessionFileStore
#import phpserialize
from phpsessionencode.PHPUnserialize import PHPUnserialize
from phpsessionencode.PHPSerialize import PHPSerialize
from django.core.exceptions import SuspiciousOperation

class SessionStore(SessionFileStore):
    """ 
    Howdy pardner! Speaking of pardners, I subclass the SessionStore 
class in the file session backend. 
    This allows me intercept the decode and encode methods to grab the 
PHP sessions and use them. 
    So, in a way, this makes me PHP's pardner, also. 
    """
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)
        # override the file_prefix
        self.file_prefix = 'sess_'
    
    def decode(self, session_data):
        #return phpserialize.unserialize(session_data)
        u = PHPUnserialize()
        return u.session_decode(session_data)
    
    
    
    def encode(self, session_dict):
        """
        Encode the session using the phpsessionencode package, object PHPSerialize
        """
        #return phpserialize.serialize(session_dict)
        s = PHPSerialize()
        return s.session_encode(session_dict)

#    def load(self):
#            session_data = {}
#            try:
#                session_file = open(self._key_to_file(), "rb")
#                
#                try:
#                    file_data = session_file.read()
#                    # Don't fail if there is no data in the session file.
#                    # We may have opened the empty placeholder file.
#                    if file_data:
#                        try:
#                            session_data = self.decode(file_data)
#                        except (EOFError, SuspiciousOperation):
#                            self.create()
#                finally:
#                    session_file.close()
#            except IOError:
#                raise Exception('''The session file could not be open. 
#                                Check that you have root permissions''')
#            return session_data
#
# 
#    def load(self):
#        session_data = {}
#        try:
#            session_file = open(self._key_to_file(), "rb")
#            try:
#                file_data = session_file.read()
#                 # Don't fail if there is no data in the session file.
#                 # We may have opened the empty placeholder file.
#                if file_data:
#                    try:
#                        session_data = self.decode(file_data)
#                    except (EOFError, SuspiciousOperation):
#                        self.create()
#            finally:
#                session_file.close()
#        except IOError:
#            pass
#        return session_data