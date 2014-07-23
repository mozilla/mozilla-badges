from django.conf.urls.defaults import patterns, url, include

from mozbadges.views import placeholder_view
import views


urlpatterns = patterns('',
    (r'^awards', include(patterns('',
        # /awards.json
        url(r'^\.json$', placeholder_view, name='json'),

        (r'^/', include(patterns('',
            # /awards/
            url(r'^$', placeholder_view, name='all'),

            (r'^(?P<award>[a-z0-9]{8})', include(patterns('',
                # /awards/{award}.json
                url(r'^\.json$', placeholder_view, name='json'),

                (r'^/', include(patterns('', 
                    # /awards/{award}/
                    url(r'^$', placeholder_view, name='detail'),

                    # /awards/{award}/delete/
                    url(r'^delete/$', placeholder_view, name='delete'),
                ))),
            ), namespace='award', app_name='award')),
        ))),
    ), namespace='awards', app_name='awards')),
)
