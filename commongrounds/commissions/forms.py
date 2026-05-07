from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job, JobApplication


JobFormSet = inlineformset_factory(Commission, Job, fields=['role', 'manpower_required'],
                                   extra=2)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []
