from django.contrib.auth.models import User
from django.db import models

from mozbadges.utils.decorators import public_attributes


@public_attributes('username', get_full_name='name', get_absolute_url='url')
class Person (User):
    class Meta:
        proxy = True
        verbose_name_plural = "people"

    @models.permalink
    def get_absolute_url (self):
        return ('people:person:detail', [self.username])

    @models.permalink
    def get_json_url (self):
        return ('people:person:json', [self.username])
