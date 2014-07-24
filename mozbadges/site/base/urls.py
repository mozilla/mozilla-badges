from django.conf.urls.defaults import patterns, url

from mozbadges.views import placeholder_view

import views


urlpatterns = patterns('',
    # /
    url(r'^$', views.home, name='home'),
    # /create/
    url(r'^create/$', views.create, name='create'),
    # /claim/
    url(r'^claim/$', views.claim, {'code': None}, name='claim'),
    # /claim/{code}/
    url(r'^claim/(?P<code>[^/]+)/$', views.claim, name='claim_code'),
    # /studio/
    url(r'^studio/$', views.studio, name='studio'),
)
