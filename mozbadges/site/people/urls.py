from django.conf.urls.defaults import patterns, url, include

from mozbadges.views import placeholder_view
import views


urlpatterns = patterns('',
    (r'^people', include(patterns('',
        (r'^/', include(patterns('',
            # /people/
            url(r'^$', placeholder_view, name='all'),

            (r'^(?P<person>[^ /]+)/', include(patterns('',
                # /people/{person}/
                url(r'^$', placeholder_view, name='detail'),

                # /people/{person}/badges/
                url(r'^badges/$', placeholder_view, name='badges'),
                # /people/{person}/awards/
                url(r'^awards/$', placeholder_view, name='awards'),
            ), namespace='person', app_name='person')),
        ))),
    ), namespace='people', app_name='people')),
)
