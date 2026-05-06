from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from accounts.decorators import role_required
from .models import EventSignup, Event
from .forms import EventSignupForm

# from .strategies import AuthenticatedPurchaseStrategy, GuestPurchaseStrategy


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
    template_name = "event_detail.html"

    #tentatatatatatatatatatative
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = EventSignupForm()
        return context
    
    #second tentative tthing
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        user = self.request.user

        ReviewForm = BookFormFactory.get_form("review", user=self.request.user)
        context['review_form'] = ReviewForm()
        context['reviews'] = BookReview.objects.filter(book=book)
        context['bookmark_count'] = Bookmark.objects.filter(book=book).count()

        if user.is_authenticated:
            context['is_contributor'] = (book.contributor == user.profile)
            context['is_bookmarked'] = Bookmark.objects.filter(
                book=book, profile=user.profile).exists()

        return context
