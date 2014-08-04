from jingo import register as jingo_register
from django_browserid.helpers import browserid_button, browserid_info

from mozbadges import utils
from mozbadges.compat import _lazy as _, reverse


@jingo_register.function
def time_since(*args, **kwargs):
    return utils.time_since(*args, **kwargs)


@jingo_register.function
def persona_info():
    # For consistency
    return browserid_info()


@jingo_register.function
def persona_login(text='Sign in', color=None, next='',
                  link_class='browserid-login persona-button', attrs=None, fallback_href='#'):
    if color:
        if 'persona-button' not in link_class:
            link_class += ' persona-button {0}'.format(color)
        else:
            link_class += ' ' + color
    return browserid_button(_(text), next, link_class, attrs, fallback_href)


@jingo_register.function
def persona_logout(text='Sign out', next='', link_class='browserid-logout', attrs=None):
    return browserid_button(_(text), next, link_class, attrs, reverse('browserid.logout'))
