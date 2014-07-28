from django import forms

from mozbadges.forms.models import GroupedModelChoiceField
from mozbadges.site.people.models import Person, Community


class WelcomeForm(forms.ModelForm):
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
