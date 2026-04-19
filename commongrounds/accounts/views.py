from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['display_name']
    template_name = 'profile_update.html'