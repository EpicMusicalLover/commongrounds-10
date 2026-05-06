from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication
from .forms import JobFormSet


class CommissionListView(ListView):
    model = Commission
    template_name = "commission_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user.profile
            context["your_commissions"] = Commission.objects.filter(
                maker=self.request.user.profile
            )
            context["your_applications"] = Commission.objects.filter(
                jobs__application__applicant=self.request.user.profile
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

        sum_of_manpower = 0
        accepted = 0
        open_manpower = 0
        commission_pk = self.kwargs['pk']
        for jobs in Job.objects.filter(commission=Commission.objects.get(pk=commission_pk)):
            sum_of_manpower += jobs.manpower_required
            for signee in JobApplication.objects.filter(job=jobs):
                if signee.status == "Accepted":
                    accepted += 1

        open_manpower = sum_of_manpower - accepted

        context["sum_of_manpower"] = sum_of_manpower
        context["open_manpower"] = open_manpower
        return context


class CommissionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    required_role = "Commission Maker"
    model = Commission
    template_name = "commission_create.html"
    fields = [
        "title",
        "description",
        "commission_type",
        "people_required",
        "status",
        ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job'] = JobFormSet(self.request.POST)
        else:
            context['job'] = JobFormSet()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        context = self.get_context_data()
        formset = context['job']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
