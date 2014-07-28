# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.
PROJECT_MODULE = 'mozbadges'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'constance.context_processors.config',
]

INSTALLED_APPS = list(INSTALLED_APPS) + [
    # Application base, containing global templates.
    '%s.site.account' % PROJECT_MODULE,
    '%s.site.auth' % PROJECT_MODULE,
    '%s.site.badges' % PROJECT_MODULE,
    '%s.site.base' % PROJECT_MODULE,
    '%s.site.people' % PROJECT_MODULE,
    '%s.site.teams' % PROJECT_MODULE,

    'south',
    'django.contrib.admin',
    'constance',
    'constance.backends.database',
]

# Note! If you intend to add `south` to INSTALLED_APPS,
# make sure it comes BEFORE `django_nose`.
#INSTALLED_APPS.remove('django_nose')
#INSTALLED_APPS.append('django_nose')


LOCALE_PATHS = (
    os.path.join(ROOT, PROJECT_MODULE, 'locale'),
)

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = (
    'admin',
    'registration',
    'browserid',
)

# BrowserID configuration
AUTHENTICATION_BACKENDS = (
    # This is a wrapper around `django.contrib.auth.backends.ModelBackend`,
    # but uses our proxied Person model instead of a regular User
    'django_browserid.auth.BrowserIDBackend',
    'mozbadges.auth.backends.PersonModelBackend',
)

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = 'account:welcome'
LOGIN_REDIRECT_URL_FAILURE = '/'

BROWSERID_VERIFY_CLASS = 'mozbadges.auth.views.Verify'

TEMPLATE_CONTEXT_PROCESSORS += (
    # other possible context processors here...
)

AUTH_USER_MODEL = 'people.Person'

# Should robots.txt deny everything or disallow a calculated list of URLs we
# don't want to be crawled?  Default is false, disallow everything.
# Also see http://www.google.com/support/webmasters/bin/answer.py?answer=93710
ENGAGE_ROBOTS = False

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS['messages'] = [
    ('%s/**.py' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_python'),
    ('%s/**/templates/**.html' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_template'),
    ('templates/**.html',
        'tower.management.commands.extract.extract_tower_template'),
]

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable JS files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]

LOGGING = {
    'loggers': {
        'playdoh': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django_browserid': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

CONSTANCE_CONFIG = dict(
    MOZILLIANS_API_BASE_URL = (
        'https://mozillians.org/api/v1',
        'Mozillians.org API base URL',
    ),
    MOZILLIANS_API_APPNAME = (
        '',
        'Mozillians.org API app name',
    ),
    MOZILLIANS_API_KEY = (
        '',
        'Mozillians.org API key',
    ),
    MOZILLIANS_API_CACHE_KEY_PREFIX = (
        'mozillians_api',
        'Mozillians.org API result cache key prefix',
    ),
    MOZILLIANS_API_CACHE_TIMEOUT = (
        1800,
        'Mozillians.org API result cache timeout',
    ),
)

def username_algo(email):
    from mozbadges.auth import generate_username
    return generate_username(email)

BROWSERID_USERNAME_ALGO = username_algo
