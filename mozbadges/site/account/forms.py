from django import forms

from mozbadges.forms.models import GroupedModelChoiceField
from mozbadges.site.people.models import Person, Community


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
                        help_text='')
    display_name = forms.CharField(
                        required=False,
                        label='Display Name',
                        max_length=50,
                        help_text='This is what users across the site will see. We\'ll use your username if you leave this blank.')
    bio = forms.CharField(
                        widget=forms.Textarea,
                        required=False,
                        help_text='A little bit about yourself')
    community = GroupedModelChoiceField(
                        queryset=Community.objects.order_by('region', 'name'),
                        group_by='region',
                        required=False,
                        empty_label='-- None --',
                        help_text='This might be where you live, or another group you are particularly involved with.')


class WelcomeForm(UserProfileForm):
    pass


class EditProfileForm(UserProfileForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            if not instance.can_change_username():
                self.fields['username'].widget.attrs['disabled'] = True
                self.fields['username'].required = False
            remaining = instance.username_changes_remaining() or 'no'
            plural = '' if remaining == 1 else 's'
            self.fields['username'].help_text += '\nYou have %s change%s remaining.' % (remaining, plural)

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and not instance.can_change_username():
            return instance.username
        else:
            return self.cleaned_data['username']

    def save(self, commit=True):
        old_username = self.initial['username']
        new_username = self.cleaned_data['username']

        if old_username != new_username:
            self.instance.username_changes += 1

        return super(EditProfileForm, self).save(commit)
