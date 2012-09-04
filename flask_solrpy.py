'''
Created on Sep 4, 2012

@author: jluker
'''
import logging
from solr import SolrConnection
from flask import g

name = __name__
logger = logging.getLogger(__name__)

class SolrConfigurationError(Exception):
    pass

class SolrConnectionError(Exception):
    pass

def _create_solr_connection(app):
    app.config.setdefault('SOLR_URL', 'http://localhost:8983/solr')
    app.config.setdefault('SOLR_PERSISTENT', True)
    app.config.setdefault('SOLR_TIMEOUT', 30)
    app.config.setdefault('SOLR_POST_HEADERS', {})
    app.config.setdefault('SOLR_MAX_RETRIES', 0)
    
    xtra_kwargs = {}
    if app.config.has_key('SOLR_SSL_CRED'):
        try:
            xtra_kwargs['ssl_key'] = app.config['SOLR_SSL_CRED'][0]
            xtra_kwargs['ssl_cert'] = app.config['SOLR_SSL_CRED'][1]
        except Exception, e:
            raise SolrConfigurationError("Bad SOLR_SSL_CRED value: %s" % (str(e)))
    if app.config.has_key('SOLR_HTTP_BASIC_AUTH'):
        try:
            xtra_kwargs['http_user'] = app.config['SOLR_HTTP_BASIC_AUTH'][0]
            xtra_kwargs['http_pass'] = app.config['SOLR_HTTP_BASIC_AUTH'][1]
        except Exception, e:
            raise SolrConfigurationError("Bad SOLR_HTTP_BASIC_AUTH value: %s" % (str(e)))
        
    return SolrConnection(
                app.config['SOLR_URL'], 
                persistent=app.config['SOLR_PERSISTENT'],
                timeout=app.config['SOLR_TIMEOUT'],
                post_headers=app.config['SOLR_POST_HEADERS'],
                max_retries=app.config['SOLR_MAX_RETRIES'],
                **xtra_kwargs
                )
        
class FlaskSolrpy(object):
    """
    Connection to a solr instance using SOLR_URL parameter defined
    in Flask configuration
    """
    
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
        else:
            self.solr = None
            
    def init_app(self, app):
        try:
            self.solr = _create_solr_connection(app)
        except Exception, e:
            raise SolrConnectionError("%s: %s" % (type(e), str(e)))
        app.before_request(self.request_start)
        
    def request_start(self):
        g.solr = self.solr
        