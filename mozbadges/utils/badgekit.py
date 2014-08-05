from urlparse import urljoin
from django.conf import settings

BADGEKIT_ROOT = urljoin(settings.BADGEKIT_API_ENDPOINT, '/systems/%s/' % settings.BADGEKIT_API_SYSTEM)

def badgekit_url(path='', *args, **kwargs):
  return urljoin(BADGEKIT_ROOT, str(path).lstrip('/').format(*args, **kwargs))