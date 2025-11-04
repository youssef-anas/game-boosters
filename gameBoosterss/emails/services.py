from typing import Dict, Iterable, Optional
import threading

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

# Celery (optional)
try:
    from celery import shared_task  # type: ignore
    CELERY_AVAILABLE = True
except Exception:
    shared_task = None
    CELERY_AVAILABLE = False


def _render_email(template_name: str, context: Dict) -> Dict[str, str]:
    html = render_to_string(template_name, context)
    text = strip_tags(html)
    return {"html": html, "text": text}


def _send_email(subject: str, recipients: Iterable[str], html: str, text: str) -> int:
    email = EmailMultiAlternatives(subject, text, getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER), list(recipients))
    email.attach_alternative(html, "text/html")
    return email.send(fail_silently=False)


def _send_email_async(subject: str, recipients: Iterable[str], template_name: str, context: Dict) -> None:
    # In test mode, send synchronously to allow assertions
    email_backend = getattr(settings, 'EMAIL_BACKEND', '')
    if 'locmem' in email_backend.lower() or 'console' in email_backend.lower() or 'filebased' in email_backend.lower():
        _send_email_sync(subject, list(recipients), template_name, context)
    elif CELERY_AVAILABLE and shared_task is not None:
        _send_email_task.delay(subject, list(recipients), template_name, context)  # type: ignore[attr-defined]
    else:
        threading.Thread(target=_send_email_sync, args=(subject, list(recipients), template_name, context), daemon=True).start()


def _send_email_sync(subject: str, recipients: Iterable[str], template_name: str, context: Dict) -> None:
    rendered = _render_email(template_name, context)
    _send_email(subject, recipients, rendered["html"], rendered["text"])


if CELERY_AVAILABLE and shared_task is not None:
    @shared_task
    def _send_email_task(subject: str, recipients: Iterable[str], template_name: str, context: Dict) -> None:  # pragma: no cover - celery tested via sync fallback
        _send_email_sync(subject, recipients, template_name, context)


# Public service functions

def send_manager_alert_email(order, title: str, message: str, extra_context: Optional[Dict] = None) -> None:
    context = {
        "order": order,
        "title": title,
        "message": message,
    }
    if extra_context:
        context.update(extra_context)
    recipients = []
    # Heuristic: all staff as managers
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        recipients = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
    except Exception:
        recipients = [getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER)]
    _send_email_async(f"Manager Alert • Order #{getattr(order, 'id', 'N/A')}", recipients, 'mails/manager_alert_mail.html', context)


def send_admin_error_email(title: str, error_message: str, extra_context: Optional[Dict] = None) -> None:
    context = {
        "title": title,
        "error_message": error_message,
    }
    if extra_context:
        context.update(extra_context)
    recipients = [getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER)]
    _send_email_async(f"Admin Alert • {title}", recipients, 'mails/admin_error_mail.html', context)


def send_client_payment_email(order, transaction) -> None:
    if not getattr(order, 'customer', None) or not getattr(order.customer, 'email', None):
        return
    context = {
        "order": order,
        "transaction": transaction,
        "client": order.customer,
    }
    _send_email_async("Payment Confirmation", [order.customer.email], 'mails/client_payment_mail.html', context)


def send_booster_payout_email(order, transaction) -> None:
    booster = getattr(order, 'booster', None)
    if not booster or not getattr(booster, 'email', None):
        return
    context = {
        "order": order,
        "transaction": transaction,
        "booster": booster,
    }
    _send_email_async("Payout Confirmation", [booster.email], 'mails/booster_payout_mail.html', context)


