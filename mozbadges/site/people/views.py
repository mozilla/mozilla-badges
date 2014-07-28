from mozbadges.views.generic.detail import HybridDetailView
from mozbadges.views.generic.list import HybridListView

from models import Person


class PersonDetailView(HybridDetailView):
    model = Person
    slug_field = 'username'
    slug_url_kwarg = 'person'
    context_object_name = 'person'
    template_name = 'people/detail.html'


class PersonListView(HybridListView):
    model = Person
    context_object_name = 'people'
    template_name = 'people/list.html'


person_detail = PersonDetailView.as_view()
person_list = PersonListView.as_view()
