from django.conf.urls.defaults import patterns, url, include

from mozbadges.views import placeholder_view
import views


urlpatterns = patterns('',
    (r'^people', include(patterns('',
        (r'^/', include(patterns('',
            # /people/
            url(r'^$', placeholder_view, name='all'),

            (r'^(?P<person>[^ /]+)', include(patterns('',
                (r'^/', include(patterns('',
                    # /people/{person}/
                    url(r'^$', placeholder_view, name='detail'),

                    (r'^badges', include(patterns('',
                        # /people/{person}/badges/
                        url(r'^/$', placeholder_view, name='all'),
                        # /people/{person}/badges.json
                        url(r'^\.json$', placeholder_view, name='json'),
                    ), namespace='badges', app_name='badges')),

                    (r'^awards', include(patterns('',
                        # /people/{person}/awards/
                        url(r'^/$', placeholder_view, name='all'),
                        # /people/{person}/awards.json
                        url(r'^\.json$', placeholder_view, name='json'),
                    ), namespace='awards', app_name='awards')),
                ))),
            ), namespace='person', app_name='person')),
        ))),
    ), namespace='people', app_name='people')),
)
