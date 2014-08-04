from django import http
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.utils.text import capfirst
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


def cleanup_json(data):
    # Just `unicode` anything that can't otherwise be handled.
    # Solves the commonest problem of proxied translation strings, if nothing else.
    return unicode(data)


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
        blacklisted = ['object_list', 'object', 'is_paginated', 'paginator', 'page_obj', 'view']
        data = dict([(key, value) for key, value in context.iteritems()
                                    if key not in blacklisted])

        if 'object_list' in context:
            data_key = self.get_context_object_name(context['object_list']) or 'object_list'
        elif 'object' in context:
            data_key = self.get_context_object_name(context['object']) or 'object'

        data['$'+_('data')] = data_key
        data[data_key] = serialize(context.get(data_key))

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

        return json.dumps(data, cls=DjangoJSONEncoder, default=cleanup_json)

    def get_page_link(self, page):
        path = self.request.path
        query = self.request.GET.copy()
        if page == 1:
            del query['page']
        else:
            query['page'] = page
        return urlunparse(('', '', path, '', urlencode(query), ''))


class ContextMixin(object):
    def get_context_data(self, **kwargs):
        context = {}

        try:
            context.update(self.context_data)
        except:
            pass

        if 'page_title' not in context:
            if hasattr(self, 'page_title'):
                context['page_title'] = self.page_title
            elif hasattr(self, 'model') and self.model is not None:
                context['page_title'] = capfirst(self.model._meta.verbose_name_plural)
            elif hasattr(self, 'object') and self.object is not None:
                context['page_title'] = unicode(self.object)

        context.update(super(ContextMixin, self).get_context_data(**kwargs))
        return context
