from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from notification.models import Notice

from mozbadges.utils.decorators import render_to
from mozbadges.views.generic.detail import HybridDetailView
from mozbadges.views.generic.list import HybridListView

class NotificationListView(HybridListView):
    model = Notice
    template_name = 'account/notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    page_title = 'Messages'

    def get_queryset(self):
        return self.model.objects.notices_for(self.request.user, on_site=True)


class NotificationDetailView(HybridDetailView):
    model = Notice
    template_name = 'account/notifications/detail.html'
    context_object_name = 'notification'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def render_to_response(self, context, **response_kwargs):
        if self.object.unseen:
            self.object.unseen = False
            self.object.save()
        return super(NotificationDetailView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotificationDetailView, self).get_context_data(**kwargs)
        context['previous'] = self.object.get_previous()
        context['next'] = self.object.get_next()
        return context

    def get_queryset(self):
        qs = super(NotificationDetailView, self).get_queryset()
        return qs.filter(recipient=self.request.user)


notice_list = login_required(NotificationListView.as_view())
notice_detail = login_required(NotificationDetailView.as_view())


def mark_all_as_read(request):
    # notification_views.mark_all_as_read(request)
    # return redirect('account:notifications:all')
    pass


def mark_as_read(request, slug=None):
    # notification_views.mark_as_read(request, slug)
    # return redirect('account:notifications:all')
    pass


def mark_as_read(request, slug=None):
    # notification_views.mark_as_unread(request, slug)
    # return redirect('account:notifications:all')
    pass
