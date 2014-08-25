from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models import permalink
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, DeleteView

from mozbadges.compat import reverse, _
from mozbadges.utils.decorators import requires_user
from mozbadges.views.generic.base import ContextMixin, OwnerMixin
from mozbadges.views.generic.detail import HybridDetailView
from mozbadges.views.generic.list import HybridListView

from valet_keys.forms import KeyForm
from valet_keys.models import Key


@permalink
def get_url_for_key(key):
    return ('account:keys:detail', [key.slug])

Key.get_absolute_url = get_url_for_key


class KeyListView(OwnerMixin, HybridListView):
    model = Key
    template_name = 'account/keys/list.html'
    context_object_name = 'keys'
    paginate_by = 10
    page_title = _('My API keys')


class KeyDetailView(OwnerMixin, HybridDetailView):
    model = Key
    template_name = 'account/keys/detail.html'
    context_object_name = 'key'
    slug_field = 'slug'
    slug_url_kwarg = 'key'
    page_title = _('Key history')

    def get_context_data(self, **kwargs):
        context = super(KeyDetailView, self).get_context_data(**kwargs)
        context['actions'] = self.object.history.all()
        return context


class KeyCreateView(ContextMixin, CreateView):
    form_class = KeyForm
    model = Key
    template_name = 'account/keys/create.html'
    page_title = _('New key')

    def form_valid(self, form):
        messages.success(self.request, _('Key successfully created'))

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        secret = self.object.generate_secret()
        self.object.save()

        context = self.get_context_data(form=form)
        context['secret'] = secret
        return self.render_to_response(context)


class KeyDeleteView(OwnerMixin, ContextMixin, DeleteView):
    model = Key
    template_name = 'account/keys/delete.html'
    context_object_name = 'key'
    slug_field = 'slug'
    slug_url_kwarg = 'key'
    page_title = _('Delete key')
    success_url = reverse_lazy('account:keys:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Key successfully deleted'))
        return super(KeyDeleteView, self).delete(request, *args, **kwargs)


key_list = requires_user(KeyListView.as_view())
detail = requires_user(KeyDetailView.as_view())
create = requires_user(KeyCreateView.as_view())
delete = requires_user(KeyDeleteView.as_view())

@requires_user
def disable(request, key):
    key = get_object_or_404(Key, slug=key, user=request.user)
    if not key.is_disabled:
        key.is_disabled = True
        key.save()
        request.log_action(key, notes='Key disabled')
    return HttpResponseRedirect(reverse('account:keys:detail', args=(key.slug,)))

@requires_user
def activate(request, key):
    key = get_object_or_404(Key, slug=key, user=request.user)
    if key.is_disabled:
        key.is_disabled = False
        key.save()
        request.log_action(key, notes='Key activated')
    return HttpResponseRedirect(reverse('account:keys:detail', args=(key.slug,)))
