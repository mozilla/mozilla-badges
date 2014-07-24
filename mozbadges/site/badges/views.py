from mozbadges.views.generic.detail import HybridDetailView
from mozbadges.views.generic.list import HybridListView

from models import Badge

class BadgeDetailView(HybridDetailView):
    model = Badge
    pk_url_kwarg = 'slug'
    context_object_name = 'badge'
    template_name = 'badges/detail.html'


class BadgeListView(HybridListView):
    model = Badge
    context_object_name = 'badges'
    template_name = 'badges/list.html'


badge_detail = BadgeDetailView.as_view()
badge_list = BadgeListView.as_view()
