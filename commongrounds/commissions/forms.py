from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = [
        "title",
        "description",
        "commission_type",
        "people_required",
        "status",
        ]
        widget = { "status": forms.Select() }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "role",
            "manpower_required",
            "status",
        ]


JobFormSet = inlineformset_factory(Commission, Job, fields=['role', 'manpower_required'],
                                   extra=2)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []
