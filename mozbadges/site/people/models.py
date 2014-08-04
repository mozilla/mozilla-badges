from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

from mozbadges.compat import _
from mozbadges.mozillians import api as mozillians
from mozbadges.utils.decorators import public_attributes

MAX_USERNAME_CHANGES = getattr(settings, 'PROFILE_MAX_USERNAME_CHANGES', 3)


class Community(models.Model):
    REGIONS = (
        ('1_US_CAN', 'US and Canada'),
        ('2_LAT_AM', 'Latin America'),
        ('3_EUR', 'Europe'),
        ('4_ASIA_SP', 'Asia and South Pacific'),
        ('5_A_ME', 'Africa and Middle East'),
        ('6_OTHER', 'Other'),
    )
    code = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    region = models.CharField(choices=REGIONS, max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'communities'

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return unicode(self.name)

    def get_mozilla_url(self):
        return 'https://www.mozilla.org/contact/communities/%s/' % self.slug


@public_attributes('username', 'display_name', 'location', 'bio', get_absolute_url='url')
class Person(AbstractUser):
    # Might change this to inherit from AbstractBaseUser, to remove `first_name`
    # and `last_name` and enforce uniqueness of `email`, but for now that seems
    # like wasted effort.

    is_new = models.BooleanField(default=True)
    display_name = models.CharField(max_length=50, blank=True)
    community = models.ForeignKey(Community, blank=True, null=True)
    bio = models.TextField(blank=True)
    username_changes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return str(self.display_name or self.username)

    def __unicode__(self):
        return unicode(self.display_name or self.username)

    def username_changes_remaining(self):
        return MAX_USERNAME_CHANGES - self.username_changes

    def can_change_username(self):
        return self.username_changes_remaining() > 0

    def get_mozillians_profile(self):
        if not hasattr(self, '_profile'):
            profiles = mozillians.get_users(email=self.email, cache_timeout=14400)
            try:
                self._profile = profiles[0]
            except IndexError:
                self._profile = None
        return self._profile

    def get_avatar(self, default=None):
        profile = self.get_mozillians_profile() or {}
        # Doing it this way handles empty `photo` properties,
        # as well non-existent ones.
        return profile.get('photo') or default

    def is_vouched(self):
        profile = self.get_mozillians_profile() or {}
        return profile.get('is_vouched', False)

    def send_message(self, notice_type, extra_content=None, sender=None, **kwargs):
        from mozbadges import notices

        if extra_content is None:
            extra_content = kwargs

        return notices.send([self], notice_type, extra_content, on_site=True, sender=sender)

    def get_messages(self):
        from notification.models import Notice
        return Notice.objects.notices_for(self, on_site=True)

    def observe(self, observed, signal='post_save'):
        from mozbadges import notices
        return notices.observe(observed, self, signal)

    def stop_observing(self, observed, signal='post_save'):
        from mozbadges import notices
        return notices.stop_observing(observed, self, signal)

    def is_observing(self, observed, signal='post_save'):
        from mozbadges import notices
        return notices.is_observing(observed, self, signal)

    @models.permalink
    def get_absolute_url(self):
        return ('people:person:detail', [self.username])

    @models.permalink
    def get_json_url(self):
        return ('people:person:json', [self.username])


@receiver(post_save, sender=Person)
def _welcome_new_user(**kwargs):
    if kwargs.get('created', False):
        kwargs['instance'].send_message('welcome')
