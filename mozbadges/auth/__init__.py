import logging

from django.contrib.auth import get_user_model
from mozbadges.mozillians import api


def generate_username(email):
    User = get_user_model()

    count = 0

    try:
        profile = api.get_users(email=email)[0]
        username = profile['username']
    except (TypeError, IndexError, KeyError):
        username = email.split('@')[0]

    while User.objects.filter(username=username).count() > 0:
        count += 1
        username = '%s%d' % (base_name, count)

    return username
