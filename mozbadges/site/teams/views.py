from mozbadges.views.generic.detail import HybridDetailView
from mozbadges.views.generic.list import HybridListView

from models import Team


class TeamDetailView(HybridDetailView):
    model = Team
    slug_url_kwarg = 'team'
    context_object_name = 'team'
    template_name = 'teams/detail.html'


class TeamListView(HybridListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'teams/list.html'


team_detail = TeamDetailView.as_view()
team_list = TeamListView.as_view()
