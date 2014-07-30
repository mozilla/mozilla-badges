from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from mozbadges.views import placeholder_view
import views


urlpatterns = patterns('',
    (r'^people', include(patterns('',
        # /people.json
        url(r'^\.json$', views.person_list, name='json'),

        (r'^/', include(patterns('',
            # /people/
            url(r'^$', views.person_list, name='all'),

            (r'^(?P<person>[^ /\.]+)', include(patterns('',
                # /people/{person}.json
                url(r'^\.json$', views.person_detail, name='json'),

                (r'^/', include(patterns('',
                    # /people/{person}/
                    url(r'^$', views.person_detail, name='detail'),

                    (r'^badges', include(patterns('',
                        # /people/{person}/badges/
                        url(r'^/$', placeholder_view, name='all'),
                        # /people/{person}/badges.json
                        url(r'^\.json$', placeholder_view, name='json'),
                    ), namespace='badges', app_name='badges')),

                    (r'^awards', include(patterns('',
                        # /people/{person}/awards/
                        url(r'^/$', '%s.site.awards.views.badge_award_list' % settings.PROJECT_MODULE, name='all'),
                        # /people/{person}/awards.json
                        url(r'^\.json$', '%s.site.awards.views.badge_award_list' % settings.PROJECT_MODULE, name='json'),
                    ), namespace='awards', app_name='awards')),
                ))),
            ), namespace='person', app_name='person')),
        ))),
    ), namespace='people', app_name='people')),
)
