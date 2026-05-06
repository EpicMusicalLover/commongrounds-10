from django import forms

from .models import Commission


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ["title", "description",
                  "commission_type", "people_required",
                  "jobs_needed", "status",]
