import logging

import hashlib
import base64
import random
import re
import json

try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q

from django.contrib.auth.models import User as _User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.utils.translation import ugettext_lazy as _

User = getattr(settings, 'AUTH_USER_MODEL', _User)


def generate_key():
    """Generate a random API key
    see: http://jetfar.com/simple-api-key-generation-in-python/
    """
    return (base64.b64encode(hashlib.sha256(
            str(random.getrandbits(256))).digest(),
            random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD']))
            .rstrip('=='))


def hash_secret(secret):
    return hashlib.sha512(settings.SECRET_KEY + secret).hexdigest()


class Key(models.Model):
    """Authentication key"""
    user = models.ForeignKey(User, editable=False, db_index=True, blank=False,
            null=False, serialize=False)
    key = models.CharField(_("Lookup key"),
            max_length=64, editable=False, db_index=True, serialize=False)
    hashed_secret = models.CharField(_("Hashed secret"),
            max_length=128, editable=False, db_index=False, serialize=False)
    description = models.TextField(_("Description of intended use"),
            blank=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(_("slug"), max_length=8, editable=False, unique=True)


    def __unicode__(self):
        return '<Key %s %s>' % (self.user, self.key)

    @property
    def history(self):
        return KeyAction.objects.filter(key=self).order_by(created)

    def generate_secret(self):
        self.key = generate_key()
        secret = generate_key()
        self.hashed_secret = hash_secret(secret)

        if not self.pk:
            data = pickle.dumps(self.__dict__)
            self.slug = hashlib.md5(data).hexdigest()[:8]

        return secret

    def check_secret(self, secret):
        return hash_secret(secret) == self.hashed_secret

    def disable(self):
        self.is_disabled = True
        self.save()

    def log(self, action, content_object=None, notes=None):
        action = KeyAction(key=self, action=action,
                           content_object=content_object, notes=notes)
        action.save()
        return action


class KeyAction(models.Model):
    """Record of an action taken while using a key"""
    key = models.ForeignKey(Key, related_name='history', db_index=True)
    action = models.CharField(max_length=128, blank=False)
    notes = models.TextField(null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)
