from django.db import models
from django_roa import Model as ROAModel
from rest_framework import serializers
from mozbadges.utils.badgekit import badgekit_url

class Badge (ROAModel):
    timeUnitChoices = (
      ('minutes', 'Minutes'),
      ('hours', 'Hours'),
      ('days', 'Days'),
      ('weeks', 'Weeks')
    )

    evidenceTypeChoices = (
      ('URL', 'URL'),
      ('Text', 'Text'),
      ('Photo', 'Photo'),
      ('Video', 'Video'),
      ('Sound', 'Sound')
    )

    id = models.IntegerField()
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, primary_key=True)
    imageUrl = models.URLField()
    strapline = models.CharField(blank=True, max_length=255)
    earnerDescription = models.TextField()
    consumerDescription = models.TextField()
    timeValue = models.IntegerField(blank=True, null=True)
    timeUnits = models.CharField(max_length=20, blank=True, null=True, choices=timeUnitChoices)
    limit = models.IntegerField(blank=True, null=True)
    unique = models.BooleanField()
    criteriaUrl = models.URLField()
    evidenceType = models.CharField(max_length=20, blank=True, null=True, choices=evidenceTypeChoices)
    archived = models.BooleanField()
    issuer = models.CharField(max_length=255, blank=True, null=True)

    result_field_names = ['badge', 'badges']

    @staticmethod
    def serializer():
        return BadgeSerializer

    @staticmethod
    def get_resource_url_list (**kwargs): 
        if 'team' in kwargs:
            return badgekit_url('/issuer/{team}/badges', **kwargs)
        else:
            return badgekit_url('/badges')

    def get_resource_url_detail (self):
        return u"%s/%s" % (self.get_resource_url_list(), self.pk)

    @models.permalink
    def get_absolute_url (self):
        return ('badges:badge:detail', [self.slug])

    @models.permalink
    def get_json_url (self):
        return ('badges:badge:json', [self.slug])

    @models.permalink
    def get_awards_absolute_url (self):
        return ('badges:badge:awards', [self.slug])
        
    def __unicode__ (self):
        return unicode(self.name)

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'slug', 'imageUrl', 'strapline', 'earnerDescription', 'consumerDescription', 
          'timeValue', 'timeUnits', 'limit', 'unique', 'criteriaUrl', 'evidenceType', 'archived', 'issuer')