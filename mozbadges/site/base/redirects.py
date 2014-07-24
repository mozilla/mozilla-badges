from django.conf.urls.defaults import patterns
from django.http import HttpResponse, HttpResponsePermanentRedirect


def redirect (from_url, to_url, **defaults):
    def redirect (request, **kwargs):
        params = {}
        params.update(defaults)
        params.update(dict((key, value) for key, value in kwargs.items() if value is not None))
        return HttpResponsePermanentRedirect(to_url.format(**params))
    return (from_url, redirect,)


badge_actions = ('nominate', 'award', 'edit', 'edit/design', 'delete', 'awards',)
award_actions = ('delete',)

urlpatterns = patterns('',
    redirect(
        r'^badges/create/?$',
        '/create/',
    ),
    redirect(
        r'^badges/claim/?$',
        '/claim/',
    ),
    redirect(
        r'^badges/claim/(?P<code>[^/]+)/?$',
        '/claim/{code}/',
    ),
    redirect(
        r'^badges/badge/(?P<badge>[^/]+?)(?P<trailing>\.json|/)?$',
        '/badges/{badge}{trailing}',
        trailing='/'
    ),
    redirect(
        r'^badges/badge/(?P<badge>[^/]+)(?:/(?P<action>'+('|'.join(badge_actions))+'))?/?$',
        '/badges/{badge}/{action}',
    ),
    redirect(
        r'^badges/awards/?$',
        '/awards/',
    ),
    redirect(
        r'^badges/awards/(?P<award>[^/]+?)(?P<trailing>\.json|/)?$',
        '/awards/{award}{trailing}',
        trailing='/'
    ),
    redirect(
        r'^badges/badge/(?P<award>[^/]+)(?:/(?P<action>'+('|'.join(award_actions))+'))?/?$',
        '/awards/{award}/{action}',
    ),
    redirect(
        r'^profiles/profile/(?P<person>[^/]+)/?$',
        '/people/{person}/',
    ),
    redirect(
        r'^badges/users/(?P<person>[^/]+)/badges/?$',
        '/people/{person}/badges/',
    ),
    redirect(
        r'^badges/users/(?P<person>[^/]+)/awards/?$',
        '/people/{person}/awards/',
    ),
    redirect(
        r'^accounts/login/?$',
        '/account/login/',
    ),
    redirect(
        r'^browserid/verify/?$',
        '/account/login/verify/',
    ),
    redirect(
        r'^profiles/logout/?$',
        '/account/logout/',
    ),
    redirect(
        r'^profiles/profile/(?P<person>[^/]+)/edit/?$',
        '/account/edit',
    ),
    redirect(
        r'^notification/?$',
        '/account/notifications/',
    ),
    redirect(
        r'^keys/?$',
        '/account/keys/',
    ),
    redirect(
        r'^keys/new/?$',
        '/account/keys/new/',
    ),
    redirect(
        r'^keys/(?P<key>[^/]+)(?:/history)?/?$',
        '/account/keys/{key}/',
    ),
    redirect(
        r'^keys/(?P<key>[^/]+)/delete/?$',
        '/account/keys/{key}/delete/',
    ),
)
