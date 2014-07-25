from django.conf import settings
from django.core.paginator import Paginator, Page
from django.utils import six

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
            return data['objects']

    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.endpoint = 'https://mozillians.org/api/v1/'

    def _request(self, path, query={}):
        query['app_name'] = self.name
        query['app_key'] = self.key
        url = urlparse.urljoin(self.endpoint, path.lstrip('/'))
        qs = urllib.urlencode(query)
        print url, qs
        req = urllib2.Request('%s?%s' % (url, qs,))
        return json.load(urllib2.build_opener().open(req))

    def _get_dataset(self, path, page, per_page, query={}):
        q = {}
        q.update(query)
        q['limit'] = per_page
        q['offset'] = (page - 1) * per_page

        response = self._request(path, q)
        meta = response['meta']
        objects = response['objects']

        dataset = API.DataSet(path, query, meta['total_count'], self._request)
        paginator = Paginator(dataset, per_page)
        return Page(objects, page, paginator)

    def get_users(self, page=1, per_page=20, **query):
        return self._get_dataset('/users/', page, per_page, query)

    def get_user(self, id):
        return self._request('/users/%d/' % id)

    def get_groups(self, page=1, per_page=20, order_by='id'):
        return self._get_dataset('/groups/', page, per_page, {order_by: order_by})

    def get_group(self, id):
        return self._request('/groups/%d/' % id)

    def get_skills(self, page=1, per_page=20, order_by='id'):
        return self._get_dataset('/skills/', page, per_page, {order_by: order_by})

    def get_skill(self, id):
        return self._request('/skills/%d/' % id)


api = API(settings.MOZILLIANS_APP_NAME, settings.MOZILLIANS_APP_KEY)
