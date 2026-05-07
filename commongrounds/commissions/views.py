from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobApplicationForm, JobFormSet


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
                jobs__application__applicant=self.request.user.profile
            ).exclude(
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
        jobs = self.object.jobs.all()

        sum_of_manpower = sum(job.manpower_required for job in jobs)
        accepted = sum(
            job.application.filter(status="Accepted").count() for job in jobs
        )

        context['jobs'] = jobs
        context["sum_of_manpower"] = sum_of_manpower
        context["open_manpower"] = sum_of_manpower - accepted

        if 'application_form' not in context:
            context["application_form"] = JobApplicationForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('accounts:register')
        
        if request.user.profile == self.object.maker:
            return self.render_to_response(self.get_context_data())

        job_id = request.POST.get('job_id')
        try:
            job = self.object.jobs.get(pk=job_id)
        except Job.DoesNotExist:
            return self.render_to_response(self.get_context_data())
        
        if job.not_full():
            JobApplication.objects.get_or_create(
                applicant=request.user.profile,
                job=job,
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
    form_class = CommissionForm
    
    def get_queryset(self):
        return Commission.objects.filter(maker=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in context:
            context['formset'] = JobFormSet()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommissionForm(request.POST, instance=self.object)
        formset = JobFormSet(request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            commission = form.save()
            formset.save()

            commission_jobs = commission.jobs.all()
            if commission_jobs.exists() and all(job.status == "Full" for job in commission_jobs):
                commission.status = "Full"
                commission.save()
            return redirect(commission.get_absolute_url())

        return self.render_to_response(self.get_context_data(form=form, formset=formset))
    