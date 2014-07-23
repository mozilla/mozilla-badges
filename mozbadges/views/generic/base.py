from django import http
from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils import simplejson as json
from django.utils.translation import ugettext as _
from urllib import urlencode
from urlparse import urlunparse


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert passed context into JSON string"
        data_key = self.context_object_name
        data = {
            '$'+_('data'): data_key,
            data_key: context.get(data_key)
        }

        try:
            # Add pagination information to data
            page_obj = context['page_obj']
            data['$'+_('page')] = page_obj.number
            data['$'+_('pages')] = page_obj.paginator.num_pages
            if page_obj.has_previous():
                data['$'+_('previous')] = self.get_page_link(page_obj.previous_page_number())
            if page_obj.has_next():
                data['$'+_('next')] = self.get_page_link(page_obj.next_page_number())
        except KeyError:
            # If no pagination is in use, ignore it
            pass

        return json.dumps(data, default=self.complex_dumps_default)

    def get_page_link(self, page):
        path = self.request.path
        query = self.request.GET.copy()
        if page == 1:
            del query['page']
        else:
            query['page'] = page
        return urlunparse(('', '', path, '', urlencode(query), ''))

    def complex_dumps_default(self, obj):
        if isinstance(obj, QuerySet):
            return list(obj)

        # This needs a bit of work - rather naive object dump
        if isinstance(obj, Model):
            return dict(((key, value) for key, value in obj.__dict__.iteritems() if not key.startswith('_')))

        return str(type(obj))


