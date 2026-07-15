import re

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Booking, ContactMessage, UserProfile

User = get_user_model()
PHONE_RE = re.compile(r"^\+?[0-9\s().-]{7,30}$")


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150)
    password = forms.CharField(strip=False)
    remember = forms.BooleanField(required=False)

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            return cleaned_data

        existing_user = User.objects.filter(email__iexact=email).first()
        if existing_user is None:
            raise ValidationError("Invalid email or password.")

        self.user_cache = authenticate(
            self.request,
            username=existing_user.get_username(),
            password=password,
        )
        if self.user_cache is None:
            raise ValidationError("Invalid email or password.")
        if not self.user_cache.is_active:
            raise ValidationError("This account is disabled.")

        return cleaned_data

    def get_user(self):
        return self.user_cache


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    password = forms.CharField(strip=False)
    password_confirm = forms.CharField(strip=False)
    phone = forms.CharField(max_length=30)

    def clean_full_name(self):
        full_name = " ".join(self.cleaned_data["full_name"].split())
        if len(full_name) < 2:
            raise ValidationError("Enter your full name.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not PHONE_RE.fullmatch(phone):
            raise ValidationError("Enter a valid phone number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

        if password:
            try:
                validate_password(password)
            except ValidationError as error:
                self.add_error("password", error)

        return cleaned_data

    def save(self):
        email = self.cleaned_data["email"]
        full_name = self.cleaned_data["full_name"]
        name_parts = full_name.split(maxsplit=1)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=self.cleaned_data["password"],
            first_name=name_parts[0],
            last_name=name_parts[1] if len(name_parts) > 1 else "",
        )
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            phone=self.cleaned_data["phone"],
        )
        return user


class BookingForm(forms.ModelForm):
    people = forms.IntegerField(min_value=1, max_value=20)

    class Meta:
        model = Booking
        fields = ("name", "email", "phone", "people", "date", "time")

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not PHONE_RE.fullmatch(phone):
            raise ValidationError("Enter a valid phone number.")
        return phone

    def clean_date(self):
        booking_date = self.cleaned_data["date"]
        if booking_date < timezone.localdate():
            raise ValidationError("The booking date cannot be in the past.")
        return booking_date


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "message")

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone and not PHONE_RE.fullmatch(phone):
            raise ValidationError("Enter a valid phone number.")
        return phone
