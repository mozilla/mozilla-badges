try:
    from tower import ugettext as _
except ImportError:
    from django.utils.translation import ugettext as _

try:
    from tower import ugettext_lazy as _lazy
except ImportError:
    from django.utils.translation import ugettext_lazy as _lazy

try:
    import django.utils.simplejson as json
except ImportError: # Django 1.5 no longer bundles simplejson
    import json

try:
    from funfactory.urlresolvers import reverse
except ImportError:
    from django.core.urlresolvers import reverse

