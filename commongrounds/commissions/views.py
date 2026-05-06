from django.views.generic import DetailView, CreateView, UpdateView, ListView
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
