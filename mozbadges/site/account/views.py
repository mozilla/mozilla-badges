from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, resolve_url
from django.views.generic.edit import UpdateView

from forms import WelcomeForm
from mozbadges.site.people.models import Person


class WelcomeView(UpdateView):
    model = Person
    template_name = 'account/welcome.html'
    form_class = WelcomeForm
    success_url = 'home'

    def get(self, request, *args, **kwargs):
        if not request.user.is_new:
            next = request.REQUEST.get(REDIRECT_FIELD_NAME, self.success_url)
            return redirect(resolve_url(next))

        request.user.is_new = False
        request.user.save()
        return super(WelcomeView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'skip':
            # Clear all the data out, except for the username
            # This will then be an essentially blank but valid submission.
            Data = type(request.POST)
            request.POST = Data('username=%s' % request.user.username)

        return super(WelcomeView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(WelcomeView, self).get_context_data(**kwargs)
        profile = self.request.user.get_mozillians_profile() or {}
        context['profile_link'] = profile.get('url', None)
        return context

    def get_initial(self):
        user = self.request.user
        profile = self.request.user.get_mozillians_profile() or {}

        initial = {
            'display_name': profile.get('full_name', ''),
            'bio': profile.get('bio'),
            'community': profile.get('country', '').upper(),
        }

        return initial

    def form_valid(self, form):
        # TODO - add notification for user

        return super(WelcomeView, self).form_valid(form)

welcome = login_required(WelcomeView.as_view())
