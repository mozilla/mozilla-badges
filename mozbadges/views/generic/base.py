from django import http
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from urllib import urlencode
from urlparse import urlunparse

from mozbadges.compat import _, json
from mozbadges.utils.serializers.public import Serializer


def serialize(data):
    s = Serializer()

    if isinstance(data, Model):
        # Django serializers don't do well with single instances, unfortunately
        return s.serialize([data]).pop()
    return s.serialize(data)


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
            data_key: serialize(context.get(data_key))
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
        except (KeyError, AttributeError,):
            # If no pagination is in use, ignore it
            pass

        return json.dumps(data, cls=DjangoJSONEncoder)

    def get_page_link(self, page):
        path = self.request.path
        query = self.request.GET.copy()
        if page == 1:
            del query['page']
        else:
            query['page'] = page
        return urlunparse(('', '', path, '', urlencode(query), ''))
