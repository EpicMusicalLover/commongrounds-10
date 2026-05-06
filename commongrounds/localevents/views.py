from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = "event_list.html"


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"
