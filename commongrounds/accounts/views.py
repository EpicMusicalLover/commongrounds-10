from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['display_name']
    template_name = 'profile_update.html'

class RegisterView(CreateView): #temporary
    model = User
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        return super().form_valid(form)