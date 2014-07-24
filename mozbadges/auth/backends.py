from django.contrib.auth.backends import ModelBackend

from mozbadges.site.people.models import Person


class PersonModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            return None
