from django.contrib.auth.models import User
from django.db import models

from mozbadges.utils.decorators import public_attributes


@public_attributes('username', get_full_name='name', get_absolute_url='url')
class Person (User):
    class Meta:
        proxy = True
        verbose_name_plural = 'people'

    def __str__ (self):
        return str(self.get_display_name())

    def __unicode__ (self):
        return unicode(self.get_display_name())

    def get_display_name (self):
        return self.first_name or self.username

    @models.permalink
    def get_absolute_url (self):
        return ('people:person:detail', [self.username])

    @models.permalink
    def get_json_url (self):
        return ('people:person:json', [self.username])
