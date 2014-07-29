from django.core.cache import cache
from django.core.paginator import Paginator, Page, EmptyPage
from django.utils import six

import constance.config

import hashlib
import logging
import urlparse
import urllib
import urllib2

from compat import json


class API:
    class DataSet:
        """Lazy dataset container for pagination purposes. Loads slices on demand."""
        def __init__(self, path, query, total_count, request):
            self._path = path
            self._query = query
            self._total_count = total_count
            self._request = request

        def __len__(self):
            return self._total_count

        def __getitem__(self, val):
            if not isinstance(val, (slice,) + six.integer_types):
                raise TypeError

            q = {}
            q.update(self._query)

            if isinstance(val, slice):
                q['limit'] = val.stop - val.start
                q['offset'] = val.start
            else:
                q['limit'] = 1
                q['offset'] = val

            data = self._request(self._path, q)

            if data is None:
                return None
            elif isinstance(val, slice):
                return data['objects']
            else:
                return data['objects'][0]

    def __init__(self, name=None, key=None, endpoint=None):
        self.name = name
        self.key = key
        self.endpoint = endpoint

    def _request(self, path, query={}, ignore_cache=False, cache_timeout=None):
        MOZILLIANS_API_BASE_URL = constance.config.MOZILLIANS_API_BASE_URL
        MOZILLIANS_API_APPNAME = constance.config.MOZILLIANS_API_APPNAME
        MOZILLIANS_API_KEY = constance.config.MOZILLIANS_API_KEY
        MOZILLIANS_API_CACHE_KEY_PREFIX = constance.config.MOZILLIANS_API_CACHE_KEY_PREFIX
        MOZILLIANS_API_CACHE_TIMEOUT = constance.config.MOZILLIANS_API_CACHE_TIMEOUT

        endpoint = self.endpoint or MOZILLIANS_API_BASE_URL
        app_name = self.name or MOZILLIANS_API_APPNAME
        app_key = self.key or MOZILLIANS_API_KEY
        if cache_timeout is None:
            cache_timeout = MOZILLIANS_API_CACHE_TIMEOUT

        if not app_name or not app_key:
            logging.warning('Missing Mozillians app name or key')
            return None

        query['app_name'] = app_name
        query['app_key'] = app_key

        base = urlparse.urljoin(endpoint.rstrip('/') + '/', path.lstrip('/'))
        qs = urllib.urlencode(sorted([(key, value) for key, value in query.iteritems()]))
        url = '%s?%s' % (base, qs,)

        cache_key = '%s:%s' % (MOZILLIANS_API_CACHE_KEY_PREFIX,
                               hashlib.md5(url.encode('utf-8')).hexdigest())

        content = None if ignore_cache else cache.get(cache_key)

        if not content:
            try:
                request = urllib2.Request(url)
                response = urllib2.urlopen(request)
                content = response.read()
                cache.set(cache_key, content, cache_timeout)
            except urllib2.URLError as e:
                logging.error('Mozillians request failed:\n - %s\n - %s', e, url)
                return None

        try:
            return json.loads(content)
        except ValueError as e:
            logging.error('Parsing Mozillians response failed:\n - %s\n - %s', e, url)
            return None

    def _get_dataset(self, path, page, per_page, query={}, cache_timeout=None):
        q = {}
        q.update(query)
        q['limit'] = per_page
        q['offset'] = (page - 1) * per_page

        response = self._request(path, q)

        if response is None:
            response = {
                'meta': {'total_count': 0},
                'objects': [],
            }

        meta = response['meta']
        objects = response['objects']

        dataset = API.DataSet(path, query, meta['total_count'], self._request)
        paginator = Paginator(dataset, per_page)
        return Page(objects, paginator.validate_number(page), paginator)

    def get_users(self, page=1, per_page=20, cache_timeout=None, **query):
        return self._get_dataset('/users/', page, per_page, query, cache_timeout)

    def get_user(self, id, cache_timeout=None):
        return self._request('/users/%d/' % id, cache_timeout=cache_timeout)

    def get_groups(self, page=1, per_page=20, order_by='id', cache_timeout=None):
        return self._get_dataset('/groups/', page, per_page, {order_by: order_by}, cache_timeout)

    def get_group(self, id, cache_timeout=None):
        return self._request('/groups/%d/' % id, cache_timeout=cache_timeout)

    def get_skills(self, page=1, per_page=20, order_by='id', cache_timeout=None):
        return self._get_dataset('/skills/', page, per_page, {order_by: order_by}, cache_timeout)

    def get_skill(self, id, cache_timeout=None):
        return self._request('/skills/%d/' % id, cache_timeout=cache_timeout)


api = API()
