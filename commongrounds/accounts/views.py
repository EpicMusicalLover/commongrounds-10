from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import RegisterForm
from .models import Profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['display_name']
    template_name = 'profile_update.html'
    def get_object(self):
        return self.request.user.profile
    def get_success_url(self):
        return f"/accounts/{self.object.user.username}/"

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        Profile.objects.get_or_create(user=self.object, role=form.cleaned_data['role'])
        return super().form_valid(form)