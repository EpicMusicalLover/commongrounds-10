from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobForm, JobFormSet, JobApplicationForm


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

        jobs = self.object.jobs.all()
        context['jobs'] = jobs

        if (
            self.request.user.is_authenticated
            and open_manpower > 0
            ):
            context["form"] = JobApplicationForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.is_authenticated:
            job_id = request.POST.get('job_id')
            try:
                job = self.object.jobs.get(pk=job_id)
            except Job.DoesNotExist:
                return self.render_to_response(self.get_context_data())
        
        if not job.job_full():
            JobApplication.objects.get_or_create(
                job=job,
                applicant=request.user.profile
            )
        return redirect(self.object.get_absolute_url())


class CommissionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    required_role = "Commission Maker"
    model = Commission
    template_name = "commission_create.html"
    form_class = CommissionForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in context:
            context['formset'] = JobFormSet()
        context['action'] = 'Create New Commission'
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = CommissionForm(request.POST)
        formset = JobFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            commission = form.save(commit=False)
            commission.maker = request.user.profile
            commission.save()
            formset.instance = commission
            formset.save()
            return redirect(commission.get_absolute_url())

        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class CommissionUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    required_role = "Commission Maker"
    model = Commission
    template_name = "commission_update.html"
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

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form