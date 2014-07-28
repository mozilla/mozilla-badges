from django.conf.urls.defaults import patterns, include

import base, badges, awards, people, teams, account, auth

"""Most of these apps are ok in their own namespace"""
urlpatterns = patterns('',
    (r'', include(base.redirects)),
    (r'', include(base.urls)),

    (r'', include(badges.urls)),
    (r'', include(awards.urls)),
    (r'', include(people.urls)),
    (r'', include(teams.urls)),
    
    (r'', include(account.urls)),

    (r'', include('django_browserid.urls')),
)
