from django.db import models
from urlparse import urljoin
from django.conf import settings
from django_roa import Model as ROAModel
from rest_framework import serializers

class Team (ROAModel):
    id = models.IntegerField()
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, primary_key=True)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    imageUrl = models.URLField(blank=True, null=True)

    result_field_names = ['issuer', 'issuers']

    @staticmethod
    def serializer():
        return TeamSerializer

    @staticmethod
    def get_resource_url_list (): 
        return urljoin(settings.BADGEKIT_API_ENDPOINT, '/systems/' + settings.BADGEKIT_API_SYSTEM + '/issuers')

    def get_resource_url_detail (self):
        return u"%s/%s" % (self.get_resource_url_list(), self.pk)

    @models.permalink
    def get_absolute_url (self):
        return ('teams:team:detail', [self.slug])

    @models.permalink
    def get_json_url (self):
        return ('teams:team:json', [self.slug])

    def __unicode__ (self):
        return unicode(self.name)

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'slug', 'url', 'description', 'email', 'imageUrl')