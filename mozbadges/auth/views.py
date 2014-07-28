from django.conf import settings
from django.shortcuts import resolve_url

from django_browserid.views import Verify as BrowserIDVerify


class Verify(BrowserIDVerify):
    @property
    def failure_url(self):
        """
        URL to redirect users to when login fails. This uses the value
        of ``settings.LOGIN_REDIRECT_URL_FAILURE``, and defaults to
        ``'/'`` if the setting doesn't exist.
        """

        # This is essentially the same as the standard Verify `failure_url`
        # method, but fixes the lack of `resolve_url`
        url = getattr(settings, 'LOGIN_REDIRECT_URL_FAILURE', '/')
        return resolve_url(url)

    @property
    def success_url(self):
        """
        URL to redirect users to when login succeeds. This uses the
        value of ``settings.LOGIN_REDIRECT_URL``, and defaults to
        ``'/'`` if the setting doesn't exist.
        """

        # This is essentially the same as the standard Verify `success_url`
        # method, but fixes the lack of `resolve_url`
        url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        return resolve_url(url)
