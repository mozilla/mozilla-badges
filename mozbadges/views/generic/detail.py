from django.http import Http404
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin
from os.path import splitext

from base import JSONResponseMixin


renderers = {
    '.json': JSONResponseMixin,
}


class HybridDetailView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    def render_to_response(self, context):
        _, extension = splitext(self.request.path)

        if not extension:
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)

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

        if 'page_title' not in context and self.object:
            context['page_title'] = unicode(self.object)

        context.update(super(HybridDetailView, self).get_context_data(**kwargs))
        return context
