import jwt
import time
import hashlib
import urlparse

from . import *

class JWTAuthFilter(object):
    def __init__(self, key, secret):
        self.key = key 
        self.secret = secret

    def on_request(self, request):
        url = urlparse.urlparse(request.url)
        path = url.path
        if url.query:
            path = path + '?' + url.query

        headers = {
            'typ': 'JWT',
            'alg': 'HS256'
        }

        payload = {
            'key': self.key,
            'exp': int(time.time()) + (1000 * 60),
            'method': request.method.upper(),
            'path': path
        }

        try:
            if request.body:
                payload['body'] = {
                    'alg': 'SHA256',
                    'hash': hashlib.sha256(request.body).hexdigest()
                }
        except AttributeError:
            pass
        

        signed = jwt.encode(payload, self.secret, headers=headers)

        request.headers['Authorization'] = 'JWT token="%s"' % signed

        return request

ROA_FILTERS = [ JWTAuthFilter(BADGEKIT_API_AUTH['key'], BADGEKIT_API_AUTH['secret']) ]