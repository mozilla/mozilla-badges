from django.http import Http404
from django.views.generic.list import BaseListView, MultipleObjectTemplateResponseMixin
from os.path import splitext

from base import JSONResponseMixin, ContextMixin


renderers = {
    '.json': JSONResponseMixin,
}


class HybridListView(ContextMixin, JSONResponseMixin, MultipleObjectTemplateResponseMixin, BaseListView):
    def render_to_response(self, context):
        _, extension = splitext(self.request.path)

        if not extension:
            return MultipleObjectTemplateResponseMixin.render_to_response(self, context)

        try:
            renderer = renderers[extension]
            return renderer.render_to_response(self, context)
        except KeyError:
            raise Http404
