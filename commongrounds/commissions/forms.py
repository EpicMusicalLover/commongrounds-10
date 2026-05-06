from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job


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

JobFormSet = inlineformset_factory(Commission, Job, fields=['role', 'manpower_required'],
                                   extra=2)
