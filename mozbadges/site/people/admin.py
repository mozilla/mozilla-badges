from django.contrib import admin

from models import Person, Community
from forms import PersonAdminForm

from mozbadges.compat import _


class CommunityAdmin (admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    # search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('name',)


class PersonAdmin (admin.ModelAdmin):
    form = PersonAdminForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'display_name', 'bio', 'community')}),
        (_('Status'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Community, CommunityAdmin)
admin.site.register(Person, PersonAdmin)
