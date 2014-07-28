from django.contrib.auth.forms import UserChangeForm
from models import Person


class PersonAdminForm(UserChangeForm):
    class Meta:
        model = Person
