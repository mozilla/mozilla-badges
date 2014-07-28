from django import forms

from models import Community
from fields import GroupedModelChoiceField


class CommunityAdminForm(forms.ModelForm):
    community = GroupedModelChoiceField(group_by_field='parent')
    