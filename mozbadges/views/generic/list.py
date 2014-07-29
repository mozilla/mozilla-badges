from django.http import Http404
from django.utils.text import capfirst
from django.views.generic.list import BaseListView, MultipleObjectTemplateResponseMixin
from os.path import splitext

from base import JSONResponseMixin


renderers = {
    '.json': JSONResponseMixin,
}


class HybridListView(JSONResponseMixin, MultipleObjectTemplateResponseMixin, BaseListView):
    def render_to_response(self, context):
        _, extension = splitext(self.request.path)

        if not extension:
            return MultipleObjectTemplateResponseMixin.render_to_response(self, context)

        try:
            renderer = renderers[extension]
            return renderer.render_to_response(self, context)
        except KeyError:
            raise Http404

    def get_context_data(self, **kwargs):
        context = {}

        try:
            context.update(self.context_data)
        except:
            pass

        if 'page_title' not in context and self.model:
            context['page_title'] = capfirst(self.model._meta.verbose_name_plural)

        context.update(super(HybridListView, self).get_context_data(**kwargs))
        return context
