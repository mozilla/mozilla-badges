from django.conf.urls.defaults import patterns, url

from mozbadges.views import placeholder_view


urlpatterns = patterns('',
    # /
    url(r'^$', placeholder_view, name='home'),
    # /create/
    url(r'^create/$', placeholder_view, name='create'),
    # /claim/
    url(r'^claim/$', placeholder_view, {'code': None}, name='claim'),
    # /claim/{code}/
    url(r'^claim/(?P<code>[^/]+)/$', placeholder_view, name='claim_code'),
    # /studio/
    url(r'^studio/$', placeholder_view, name='studio'),
)
