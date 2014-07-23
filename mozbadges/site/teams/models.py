from django.db import models


class Team (models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    @models.permalink
    def get_absolute_url (self):
        return ('teams:team:detail', [self.slug])

    @models.permalink
    def get_json_url (self):
        return ('teams:team:json', [self.slug])

    def __unicode__ (self):
        return unicode(self.name)
