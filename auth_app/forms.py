from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "password1", "password2"]
        labels = {
            "username": "Username",
            "first_name": "First Name",
            "password1": "Password",
            "password2": "Confirm Password",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Enter username",
                    "class": "form-control",
                    "id": "Username",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter username",
                    "class": "form-control",
                    "id": "Username",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "placeholder": "Enter password",
                    "class": "form-control",
                    "id": "Password",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "placeholder": "Confirm password",
                    "class": "form-control",
                    "id": "confirm Password",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Apply custom widget styling for inherited password fields (password1 and password2),
        since Meta.widgets doesn't affect them.
        """
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "class": "form-control",
                "id": "Password",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password",
                "class": "form-control",
                "id": "Confirm Password",
            }
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        password_confirmation = cleaned_data.get("password2")

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
