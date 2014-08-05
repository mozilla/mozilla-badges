from django.conf.urls.defaults import patterns, url, include

from mozbadges.views import placeholder_view
import views

urlpatterns = patterns('',
    (r'^awards', include(patterns('',
        # /awards.json
        url(r'^\.json$', views.award_list, name='json'),

        (r'^/', include(patterns('',
            # /awards/
            url(r'^$', views.award_list, name='all'),

            (r'^(?P<award>[\w-]+)', include(patterns('',
                # /awards/{award}.json
                url(r'^\.json$', views.award_detail, name='json'),

                (r'^/', include(patterns('', 
                    # /awards/{award}/
                    url(r'^$', views.award_detail, name='detail'),

                    # /awards/{award}/delete/
                    url(r'^delete/$', placeholder_view, name='delete'),
                ))),
            ), namespace='award', app_name='award')),
        ))),
    ), namespace='awards', app_name='awards')),
)
