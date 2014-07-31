from django.contrib.auth.forms import UserChangeForm
from models import Person


class PersonAdminForm(UserChangeForm):
    class Meta:
        model = Person

    def clean_password(self):
        if 'password' in self.initial:
            return self.initial["password"]
        return ''
