from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/auth/register/", views.register_view, name="register"),
    path("api/auth/login/", views.login_view, name="login"),
    path("api/auth/logout/", views.logout_view, name="logout"),
    path(
        "api/auth/password-reset/",
        views.password_reset_request_view,
        name="password_reset_request",
    ),
    path("api/bookings/", views.booking_create_view, name="booking_create"),
    path("api/contact/", views.contact_create_view, name="contact_create"),
    path(
        "auth/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="main/password_reset_confirm.html",
            success_url=reverse_lazy("main:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "auth/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="main/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
