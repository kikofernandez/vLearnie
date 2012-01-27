'''
Created on 02/08/2011

@author: kikofernandezreyes
'''
from piston.resource import Resource

class CsrfExemptResource(Resource):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )