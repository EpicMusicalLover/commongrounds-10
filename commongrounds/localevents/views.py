from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = "event_list.html"


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"
