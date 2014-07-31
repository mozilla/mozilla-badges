from django.conf.urls.defaults import patterns, url, include

from mozbadges.views import placeholder_view
import views


urlpatterns = patterns('',
    (r'^account/', include(patterns('',
        # /account/
        url(r'^$', placeholder_view, name='dashboard'),

        # /account/welcome/
        url(r'^welcome/$', views.welcome, name='welcome'),

        # /account/edit/
        url(r'^edit/$', views.edit_profile, name='edit'),

        # /account/settings/
        url(r'^settings/$', placeholder_view, name='settings'),

        (r'^messages/', include(patterns('',
            # /account/notifications/
            url(r'^$', views.notifications.notice_list, name='list'),
            # /account/notifications/mark_all_as_read/
            url(r'^mark_all_as_read$', placeholder_view, name='mark_all_as_read'),
            (r'^(?P<slug>[a-z0-9]{8})/', include(patterns('',
                # /account/notifications/{slug}/
                url(r'^$', views.notifications.notice_detail, name='detail'),
                # /account/notifications/{slug}/mark_as_read/
                url(r'^mark_as_read$', views.notifications.mark_as_read, name='mark_as_read'),
                # /account/notifications/{slug}/mark_as_unread/
                url(r'^mark_as_unread$', views.notifications.mark_as_unread, name='mark_as_unread'),
                # /account/notifications/{slug}/delete/
                url(r'^delete$', views.notifications.delete, name='delete'),
                # /account/notifications/{slug}/archive/
                url(r'^archive$', views.notifications.archive, name='archive'),
            ))),
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
