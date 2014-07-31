from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from notification.models import Notice

from mozbadges.compat import reverse
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
        return self.request.user.get_messages()


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
    for messages in request.user.get_messages.filter(unseen=True):
        message.unseen = False
        message.save()
    return HttpResponseRedirect(reverse('account:notifications:list'))


def delete(request, slug=None):
    message = get_object_or_404(Notice, slug=slug, recipient=request.user)
    message.delete()
    return HttpResponseRedirect(reverse('account:notifications:list'))


def archive(request, slug=None):
    message = get_object_or_404(Notice, slug=slug, recipient=request.user)
    message.archive()
    return HttpResponseRedirect(reverse('account:notifications:list'))

def mark_as_read(request, slug=None):
    message = get_object_or_404(Notice, slug=slug, recipient=request.user)
    message.unseen = False
    message.save()
    return HttpResponseRedirect(reverse('account:notifications:list'))


def mark_as_unread(request, slug=None):
    message = get_object_or_404(Notice, slug=slug, recipient=request.user)
    message.unseen = True
    message.save()
    return HttpResponseRedirect(reverse('account:notifications:list'))
