from django.conf.urls.defaults import patterns, url, include

from mozbadges.views import placeholder_view
import views


urlpatterns = patterns('',
    (r'^teams', include(patterns('',
        # /teams.json
        url(r'^\.json$', views.team_list, name='json'),
        url(r'^\.xml$', views.team_list, name='xml'),

        (r'^/', include(patterns('',
            # /teams/
            url(r'^$', views.team_list, name='all'),

            (r'^(?P<team>[^ /.]+)', include(patterns('',
                # /teams/{team}.json
                url(r'\.json$', views.team_detail, name='json'),

                (r'^/', include(patterns('',
                    # /teams/{team}/
                    url(r'^$', views.team_detail, name='detail'),

                    # /teams/{team}/badges/
                    url(r'^badges/$', placeholder_view, name='badges'),
                    # /teams/{team}/members/
                    url(r'^members/$', placeholder_view, name='members'),

                    # /teams/{team}/favorite/
                    url(r'^favorite/$', placeholder_view, name='favorite'),
                    # /teams/{team}/unfavorite/
                    url(r'^unfavorite/$', placeholder_view, name='unfavorite'),
                ))),
            ), namespace='team', app_name='team')),
        ))),
    ), namespace='teams', app_name='teams')),
)
