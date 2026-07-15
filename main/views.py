import logging

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import BookingForm, ContactForm, LoginForm, RegisterForm
from .models import MenuCategory, MenuItem, PrivateEvent, Speciality, StaticSection

logger = logging.getLogger(__name__)


def _form_errors(form):
    return {
        field: [str(message) for message in messages]
        for field, messages in form.errors.items()
    }


def _display_name(user):
    try:
        if user.profile.full_name:
            return user.profile.full_name
    except AttributeError:
        pass
    return user.get_full_name() or user.email or user.get_username()


def index(request):
    context = {
        "about": StaticSection.objects.filter(
            slug=StaticSection.ABOUT,
            is_active=True,
        ).first(),
        "team": StaticSection.objects.filter(
            slug=StaticSection.TEAM,
            is_active=True,
        ).first(),
        "specialities": Speciality.objects.filter(is_active=True),
        "menu_categories": MenuCategory.objects.filter(is_active=True),
        "menu_items": MenuItem.objects.select_related("category").filter(
            is_active=True,
            on_main=True,
            category__is_active=True,
        )[:21],
        "events": PrivateEvent.objects.filter(is_active=True),
        "today": timezone.localdate(),
    }
    return render(request, "main/index.html", context)


@require_POST
def register_view(request):
    form = RegisterForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "message": "Check the registration fields.", "errors": _form_errors(form)},
            status=400,
        )

    with transaction.atomic():
        user = form.save()
        login(request, user)

    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
    return JsonResponse(
        {
            "ok": True,
            "message": "Registration completed successfully.",
            "display_name": _display_name(user),
        },
        status=201,
    )


@require_POST
def login_view(request):
    form = LoginForm(request.POST, request=request)
    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "message": "Invalid email or password.", "errors": _form_errors(form)},
            status=400,
        )

    user = form.get_user()
    login(request, user)
    request.session.set_expiry(
        settings.SESSION_COOKIE_AGE if form.cleaned_data["remember"] else 0
    )

    return JsonResponse(
        {
            "ok": True,
            "message": "You are signed in.",
            "display_name": _display_name(user),
        }
    )


@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"ok": True, "message": "You are signed out."})


@require_POST
def password_reset_request_view(request):
    form = PasswordResetForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "message": "Enter a valid email address.", "errors": _form_errors(form)},
            status=400,
        )

    form.save(
        request=request,
        use_https=request.is_secure(),
        email_template_name="main/emails/password_reset_email.txt",
        subject_template_name="main/emails/password_reset_subject.txt",
        from_email=settings.DEFAULT_FROM_EMAIL,
        extra_email_context={"site_name": "Hungry People"},
    )

    return JsonResponse(
        {
            "ok": True,
            "message": "If this email is registered, a password reset link has been sent.",
        }
    )


@require_POST
def booking_create_view(request):
    form = BookingForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "message": "Check the booking fields.", "errors": _form_errors(form)},
            status=400,
        )

    booking = form.save(commit=False)
    if request.user.is_authenticated:
        booking.user = request.user
    booking.save()

    email_context = {"booking": booking}
    message = render_to_string("main/emails/booking_notification.txt", email_context)
    recipients = list(
        dict.fromkeys(
            address
            for address in (settings.BOOKING_NOTIFICATION_EMAIL, booking.email)
            if address
        )
    )

    email_sent = True
    try:
        send_mail(
            subject=f"New table booking: {booking.name}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
    except Exception:
        email_sent = False
        logger.exception("Booking %s was saved, but the email could not be sent.", booking.pk)

    response_message = "Your table request has been received."
    if not email_sent:
        response_message += " The request was saved, but the email notification failed."

    return JsonResponse(
        {
            "ok": True,
            "message": response_message,
            "booking_id": booking.pk,
            "email_sent": email_sent,
        },
        status=201,
    )


@require_POST
def contact_create_view(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "message": "Check the contact form fields.", "errors": _form_errors(form)},
            status=400,
        )

    contact_message = form.save(commit=False)
    if request.user.is_authenticated:
        contact_message.user = request.user
    contact_message.save()

    return JsonResponse(
        {
            "ok": True,
            "message": "Thank you. Your message has been sent.",
            "message_id": contact_message.pk,
        },
        status=201,
    )
