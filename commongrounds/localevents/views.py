from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import EventSignup, Event


class EventListView(ListView):
    model = Event
    template_name = "event_list.html"

    #tentative
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_events = Event.objects.all()
        user = self.request.user

        if user.is_authenticated:
            profile = user.profile

            events_created = all_events.filter(organizer=profile)
            events_signedup = all_events.filter(event_signup__user_profile=profile)

            events_created_ids = [event.pk for event in events_created]
            events_signedup_ids = [event.pk for event in events_signedup]

            user_event_ids = events_created_ids + events_signedup_ids

            context['all_events'] = all_events.exclude(pk__in=user_event_ids)

            context['events_created'] = events_created
            context['events_signedup'] = events_signedup
            context['all_events'] = all_events.exclude(pk__in=user_event_ids)

        else:
            context['all_events'] = all_events

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    
class EventCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    required_role = "Event Organizer"
    model = Event
    template_name = "event_create.html"
    fields = [
        "title",
        "category",
        "organizer",
        "event_image",
        "description",
        "location",
        "start_time",
        "end_time",
        "event_capacity",
        "status",
        "created_on",
        "updated_on",
    ]

    def form_valid(self, form):
        form.instance.organizer = self.request.user.profile
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    required_role = "Event Organizer"
    model = Event
    template_name = "event_update.html"
    fields = [
        "title",
        "category",
        "organizer",
        "event_image",
        "description",
        "location",
        "start_time",
        "end_time",
        "event_capacity",
        "status",
        "created_on",
        "updated_on",
    ]

    def form_valid(self, form):
        event = form.save(commit=False)
        signup_count = event.eventsignup_set.count()
        if signup_count >= event.event_capacity:
            event.status = "Full"
        else:
            event.status = "Available"

        return super().form_valid(form)
    
class EventSignUpForm():
    model = EventSignup
    #insert code

class BaseSignUpView():
    model = EventSignup
    #yeah this needs code pa