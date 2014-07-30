from django.db import models
from urlparse import urljoin
from django.conf import settings
from django_roa import Model as ROAModel
from rest_framework import serializers

from ..badges.models import Badge, BadgeSerializer
from ..people.models import Person

class Award (ROAModel):
    slug = models.CharField(max_length=255)
    email = models.EmailField(primary_key=True)
    issuedOn = models.DateTimeField()
    expires = models.DateTimeField(blank=True, null=True)
    claimCode = models.CharField(max_length=255, blank=True, null=True)
    badge = models.ForeignKey(Badge, related_name='instances')

    result_field_names = ['instance', 'instances']

    @staticmethod
    def serializer():
        return AwardSerializer

    @staticmethod
    def get_resource_url_list (**kwargs):
        if 'badge' in kwargs:
          return urljoin(settings.BADGEKIT_API_ENDPOINT, '/systems/' + settings.BADGEKIT_API_SYSTEM + '/badges/' + kwargs['badge'] + '/instances')
        elif 'person' in kwargs:
          person = Person.objects.get(username=kwargs['person'])
          return urljoin(settings.BADGEKIT_API_ENDPOINT, '/systems/' + settings.BADGEKIT_API_SYSTEM + '/instances/' + person.email)

    def get_resource_url_detail (self):
        return u"%s/%s" % (self.get_resource_url_list(), self.pk)

    @models.permalink
    def get_absolute_url (self):
        return ('awards:award:detail', [self.slug])

    @models.permalink
    def get_json_url (self):
        return ('awards:award:json', [self.slug])

    def __unicode__ (self):
        return unicode(self.name)

class AwardSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer()
    class Meta:
        model = Award
        fields = ('slug', 'email', 'issuedOn', 'expires', 'claimCode', 'badge')