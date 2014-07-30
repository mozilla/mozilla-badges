from mozbadges.views.generic.detail import HybridDetailView
from mozbadges.views.generic.list import HybridListView

from models import Award

class AwardDetailView(HybridDetailView):
    model = Award
    pk_url_kwarg = 'award'
    context_object_name = 'award'
    template_name = 'awards/detail.html'


class AwardListView(HybridListView):
    model = Award
    context_object_name = 'awards'
    template_name = 'awards/list.html'

class BadgeAwardListView(HybridListView):
    model = Award
    context_object_name = 'award'
    template_name = 'awards/badge_awards.html'

    def get_queryset(self):
        if 'badge' in self.kwargs:
          return Award.objects.filter(badge=self.kwargs['badge'])
        elif 'person' in self.kwargs:
          return Award.objects.filter(person=self.kwargs['person'])


award_detail = AwardDetailView.as_view()
award_list = AwardListView.as_view()
badge_award_list = BadgeAwardListView.as_view()
