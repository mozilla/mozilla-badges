from django.conf.urls.defaults import patterns, url, include

from mozbadges.utils.views import placeholder_view
import views


urlpatterns = patterns('',
    (r'', include(patterns('',
        # /login
        url(r'^login/$', placeholder_view, name='login'),
        # /login/verify/
        url(r'^login/verify/$', placeholder_view, name='verify'),
        # /logout/
        url(r'^logout/$', placeholder_view, name='logout'),
    ), namespace='auth', app_name='auth'))
)
