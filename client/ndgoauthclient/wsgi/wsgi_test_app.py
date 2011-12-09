"""OAuth 2.0 WSGI server middleware providing MyProxy certificates as access tokens
"""
__author__ = "R B Wilkinson"
__date__ = "09/12/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"

class WsgiTestApp(object):
    """
    Simple WSGI application that displays a token set in the WSGI environ by
    Oauth2ClientMiddleware.
    """
    method = {
        "/": 'default',
        "/cert": 'cert'
    }
    TOKEN_ENV_KEYNAME = 'oauth2client.token'
    def __init__(self, app, globalConfig, **localConfig):
        self.beakerSessionKeyName = globalConfig['beakerSessionKeyName']
        self.app = app

    def __call__(self, environ, start_response):
        methodName = self.method.get(environ['PATH_INFO'], '').rstrip()
        if methodName:
            action = getattr(self, methodName)
            return action(environ, start_response)
        elif environ['PATH_INFO'] == '/logout':
            return self.default(environ, start_response)

        elif self.app is not None:
            return self.app(environ, start_response)
        else:
            start_response('404 Not Found', [('Content-type', 'text/plain')])
            return "WSGI Test Application: invalid URI"

    def default(self, environ, start_response):
        response = "<h2>WSGI Test Application</h2>"
        start_response('200 OK', 
                       [('Content-type', 'text/html'),
                        ('Content-length', str(len(response)))])
        return [response]

    def cert(self, environ, start_response):
        cert = environ.get(self.TOKEN_ENV_KEYNAME)
        response = ["<h2>WSGI Test Application - Get Certificate</h2>"]
        if cert:
            for c in cert:
                response.append("<pre>%s</pre>" % c)
        else:
            response.append("<p>Certificate not found</p>")

        start_response('200 OK', 
                       [('Content-type', 'text/html'),
                        ('Content-length', sum([len(r) for r in response]))])
        return response

    @classmethod
    def app_factory(cls, globalConfig, **localConfig):
        return cls(None, globalConfig, **localConfig)

    @classmethod
    def filter_app_factory(cls, app, globalConfig, **localConfig):
        return cls(app, globalConfig, **localConfig)