from django.views.generic import DetailView, CreateView, UpdateView, ListView
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication


class CommissionListView(ListView):
    model = Commission
    template_name = "commission_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["your_commissions"] = Commission.objects.filter(
                maker=self.request.user.profile
            )
            context["your_applications"] = JobApplication.objects.filter(
                applicant=self.request.user.profile
            )
            context["other_commissions"] = Commission.objects.exclude(
                maker=self.request.user.profile
            )
        else:
            context["other_commissions"] = Commission.objects.all()
        return context


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commission_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class CommissionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    required_role = "Commission Maker"
    model = Commission
    template_name = "commission_create.html"

    def form_valid(self, form):
        form.instance.maker = self.request.user.profile
        return super().form_valid(form)