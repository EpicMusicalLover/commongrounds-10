from django import forms
<<<<<<< HEAD:commongrounds/diyprojects/forms.py

from .models import Project, ProjectRating, ProjectReview


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "category", "description", "materials", "steps"]


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ["comment", "image"]


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ["score"]
        widgets = {"score": forms.NumberInput(attrs={"min": 1, "max": 10})}
=======
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
        widget = {"status": forms.Select()}


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "role",
            "manpower_required",
            "status",
        ]


JobFormSet = inlineformset_factory(
    Commission, Job, fields=['role', 'manpower_required'], extra=2
    )


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []
>>>>>>> origin/CommissionRequests:commongrounds/commissions/forms.py
