from django import forms
from datetime import datetime
from .models import Comments, Bookings, UpcomingEvent, Likes
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["review_text", "rating"]
        labels = {
            "review_text": "Review",
            "rating": "Rating",
        }
        widgets = {
            "review_text": forms.TextInput(
                attrs={
                    "placeholder": "Enter your review here",
                    "class": "form-control",
                    "id": "review_text",
                }
            ),
            "rating": forms.NumberInput(
                attrs={
                    "placeholder": "Enter rating (1-5)",
                    "class": "form-control",
                    "id": "rating",
                }
            ),
        }
        error_messages = {
            "review_text": {
                "required": "Please enter your review.",
                "max_length": {
                    "message": "Review is too long. Maximum length is 500 characters.",
                    "code": "max_length",
                },
            },
            "rating": {
                "required": "Please enter a rating.",
                "invalid": {
                    "message": "Invalid rating. Please enter a number between 1 and 5.",
                    "code": "invalid",
                },
            },
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.event = kwargs.pop("event", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.user:
            comment.user = self.user
        if self.event:
            comment.event = self.event
        if commit:
            comment.save()
        return comment

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        return rating


class likesForm(forms.ModelForm):
    class Meta:
        model = Likes
        fields = ["event"]
        labels = {
            "event": "Event",
        }
        widgets = {
            "event": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "event",
                }
            ),
        }
        error_messages = {
            "event": {
                "required": "Please select an event.",
            },
        }

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop("user", None)
            self.event = kwargs.pop("event", None)
            super().__init__(*args, **kwargs)

        def save(self, commit=True):
            like = super().save(commit=False)
            if self.user:
                like.user = self.user
            if self.event:
                like.event = self.event
            if commit:
                like.save()
            return like


class BookingsForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = [
            "event_name",
            "booking_date",
            "description",
            "location",
            "event_image",
        ]
        labels = {
            "event_name": "Event Name",
            "booking_date": "Booking Date",
            "description": "Description",
            "location": "Location",
            "event_image": "Event Image",
        }
        widgets = {
            "user": forms.TextInput(
                attrs={
                    "placeholder": "Enter your name",
                    "class": "form-control",
                    "id": "user",
                }
            ),
            "booking_date": forms.DateInput(
                attrs={
                    "placeholder": "Enter booking date (YYYY-MM-DD)",
                    "class": "form-control",
                    "type": "date",
                    "id": "booking_date",
                }
            ),
            "event_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter Event name",
                    "class": "form-control",
                    "id": "booking_date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter event description",
                    "class": "form-control",
                    "id": "event_description",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "placeholder": "Enter location",
                    "class": "form-control",
                    "id": "event_location",
                }
            ),
            "event_image": forms.ClearableFileInput(
                attrs={
                    "placeholder": "Upload event image",
                    "class": "form-control",
                    "id": "event_image",
                }
            ),
        }
        error_messages = {
            "event_name": {
                "required": "Please enter your event name.",
                "max_length": {
                    "message": "Name is too long. Maximum length is 255 characters.",
                    "code": "max_length",
                },
            },
            "user": {
                "required": "Please enter your name.",
                "max_length": {
                    "message": "Name is too long. Maximum length is 100 characters.",
                    "code": "max_length",
                },
            },
            "booking_date": {
                "required": "Please enter a booking date.",
                "invalid": {
                    "message": "Invalid date format. Please use YYYY-MM-DD.",
                    "code": "invalid",
                },
            },
            "description": {
                "required": "Please enter a description.",
            },
            "location": {
                "required": "Please enter a location.",
                "max_length": {
                    "message": "Location is too long. Maximum length is 100 characters.",
                    "code": "max_length",
                },
            },
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        booking = super().save(commit=False)
        if self.user:
            booking.user = self.user
        if commit:
            booking.save()
        return booking

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get("booking_date")
        if booking_date < timezone.now().date():
            raise ValidationError("Booking date cannot be in the past.")
        return booking_date


class UpcomingEventForm(forms.ModelForm):
    class Meta:
        model = UpcomingEvent
        fields = ["name", "date", "location", "description", "image"]
        labels = {
            "name": "Event Name",
            "date": "Event Date",
            "location": "Location",
            "description": "Description",
            "image": "Event Image",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter event name",
                    "class": "form-control",
                    "id": "event_name",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "placeholder": "Enter event date (YYYY-MM-DD)",
                    "class": "form-control",
                    "id": "event_date",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "placeholder": "Enter location",
                    "class": "form-control",
                    "id": "event_location",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter event description",
                    "class": "form-control",
                    "id": "event_description",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "placeholder": "Upload event image",
                    "class": "form-control",
                    "id": "event_image",
                }
            ),
        }
        error_messages = {
            "name": {
                "required": "Please enter the event name.",
                "max_length": {
                    "message": "Event name is too long. Maximum length is 100 characters.",
                    "code": "max_length",
                },
            },
            "date": {
                "required": "Please enter the event date.",
                "invalid": {
                    "message": "Invalid date format. Please use YYYY-MM-DD.",
                    "code": "invalid",
                },
            },
            "location": {
                "required": "Please enter the location.",
                "max_length": {
                    "message": "Location is too long. Maximum length is 100 characters.",
                    "code": "max_length",
                },
            },
            "description": {
                "required": "Please enter the event description.",
            },
        }


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
                    "id": "confirm Password",
                }
            )

        error_messages = {
            "username": {
                "required": "Please enter a username.",
                "max_length": {
                    "message": "Username is too long. Maximum length is 150 characters.",
                    "code": "max_length",
                },
            },
            "first_name": {
                "required": "Please enter your first name.",
                "max_length": {
                    "message": "First name is too long. Maximum length is 30 characters.",
                    "code": "max_length",
                },
            },
            "password1": {
                "required": "Please enter a password.",
            },
            "password2": {
                "required": "Please confirm your password.",
                "password_mismatch": {
                    "message": "Passwords do not match.",
                    "code": "password_mismatch",
                },
            },
        }

        def clean(self):
            super().clean()
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                self.add_error("password2", "Passwords do not match.")
            return self.cleaned_data
