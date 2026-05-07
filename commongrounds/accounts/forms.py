from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    role = forms.ChoiceField(
        choices=[
            ("User", "User"),
            ("Market Seller", "Market Seller"),
            ("Event Organizer", "Event Organizer"),
            ("Book Contributor", "Book Contributor"),
            ("Project Creator", "Project Creator"),
            ("Commission Maker", "Commission Maker"),
        ],
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
