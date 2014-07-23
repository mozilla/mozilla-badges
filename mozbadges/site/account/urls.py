from django.conf.urls.defaults import patterns, url, include

from mozbadges.views import placeholder_view
import views


urlpatterns = patterns('',
    (r'^account/', include(patterns('',
        # /account/
        url(r'^$', placeholder_view, name='home'),

        # /account/edit/
        url(r'^edit/$', placeholder_view, name='edit'),

        # /account/settings/
        url(r'^settings/$', placeholder_view, name='settings'),

        (r'^notifications/', include(patterns('',
            # /account/notifications/
            url(r'^$', placeholder_view, name='all'),
            # /account/notifications/mark_as_read/
            url(r'^mark_as_read/$', placeholder_view, name='mark_as_read'),
            # /account/notifications/{notification}/
            url(r'^(?P<notification>[a-z0-9]+)/$', placeholder_view, name='detail'),
        ), namespace='notifications', app_name='notifications')),

        (r'^keys/', include(patterns('',
            # /keys/
            url(r'^$', placeholder_view, name='all'),
            # /keys/new/
            url(r'^new/$', placeholder_view, name='new'),

            (r'^(?P<key>[a-z0-9]+)/', include(patterns('',
                # /keys/{key}/
                url(r'^$', placeholder_view, name='detail'),
                # /keys/{key}/disable/
                url(r'^disable/$', placeholder_view, name='disable'),
            ), namespace='key', app_name='key')),
        ), namespace='keys', app_name='keys')),
    ), namespace='account', app_name='account')),
)
