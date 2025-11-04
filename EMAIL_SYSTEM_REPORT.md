## GameBoosterss Email System Report

### Overview
This report enumerates every email-sending location, its trigger, template usage, and current status across the project.

---

### 1) gameBoosterss/utils.py

```394:425:gameBoosterss/utils.py
def send_activation_code(user) -> int:
    subject = 'Activate Your Account'
    users_list = [user.email]
    secret_key = generate_random_5_digit_number()

    html_content = render_to_string('mails/activate_email_form.html', {'secret_key': secret_key, 'user':user})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content,  settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    user.activation_code = secret_key
    user.activation_time = timezone.now()
    user.save()
    return secret_key
```
- **Trigger/Event**: Account activation workflow (called wherever account activation is initiated)
- **Template**: `templates/mails/activate_email_form.html`
- **Status**: Functional (template exists)

```411:425:gameBoosterss/utils.py
def reset_password(user) -> int:
    subject = 'Password Reset'
    users_list = [user.email]
    secret_key = generate_random_5_digit_number()

    html_content = render_to_string('mails/reset_password_form.html', {'secret_key': secret_key, 'user': user})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content,  settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    user.rest_password_code = secret_key
    user.reset_password_time = timezone.now()
    user.save()
    return secret_key
```
- **Trigger/Event**: Password reset (called by reset flow)
- **Template**: `templates/mails/reset_password_form.html`
- **Status**: Functional (template exists)

```427:436:gameBoosterss/utils.py
def booster_added_message(email, password,username):
    subject = 'Your application for madboost.gg has been approved'
    users_list = [email]
    html_content = render_to_string('mails/approved_form.html', {'password': password,'username':username})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return True
```
- **Trigger/Event**: Booster application approved (called after manager/admin approves booster)
- **Template**: `templates/mails/approved_form.html`
- **Status**: Functional (template exists)

```538:556:gameBoosterss/utils.py
def send_available_to_play_mail(user, order, client_url):
    ...
    html_content = render_to_string('mails/available_mail_form.html', {...})
    ...
    email = EmailMultiAlternatives(...)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return True
```
- **Trigger/Event**: Availability request between Client and Booster
- **Template**: `templates/mails/available_mail_form.html`
- **Status**: Functional (template exists)

```558:576:gameBoosterss/utils.py
def send_message_mail(user, order, message):
    ...
    html_content = render_to_string('mails/message_mail_form.html', {...})
    ...
    email = EmailMultiAlternatives(...)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return True
```
- **Trigger/Event**: New chat message for an order (see `chat/signals.py`)
- **Template**: `templates/mails/message_mail_form.html`
- **Status**: Functional (template exists)

```578:587:gameBoosterss/utils.py
def send_mail_bootser_choose(order_name, booster):
    subject = 'You Have new Order'
    users_list = [booster.email]
    html_content = render_to_string('mails/bootser_choose_mail_form.html', {'order_name': order_name,'booster': booster, ...})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return True
```
- **Trigger/Event**: Booster assigned/choice notification to Booster
- **Template**: `templates/mails/bootser_choose_mail_form.html`
- **Status**: Functional (template exists)

---

### 2) chat/signals.py

```1:31:chat/signals.py
from gameBoosterss.utils import send_message_mail
...
@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created:
        ...
        email_thread = threading.Thread(target=send_mail_in_thread, args=(user, order, instance))
        email_thread.start()
```
- **Trigger/Event**: `Message` model `post_save` (new chat message)
- **Template**: Delegated to `send_message_mail` → `templates/mails/message_mail_form.html`
- **Status**: Functional

---

### 3) accounts/views.py (test utility)

```315:325:accounts/views.py
def test_email_view(request):
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    from_email = 'customerservice@madboost.gg'
    to_email = ['shethr999@gmail.com']

    try:
        send_mail(subject, message, from_email, to_email)
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse('An error occurred: {}'.format(str(e)))
```
- **Trigger/Event**: Manual test endpoint
- **Template**: None (plain text)
- **Status**: Functional (for manual testing)

---

### 4) gameBoosterss/smtp.py (commented example)

```14:21:gameBoosterss/smtp.py
# def send_mail(self) -> int:
#     html_content = render_to_string(self.template_name, self.context)
#     text_content = strip_tags(html_content)
#     email = EmailMultiAlternatives(self.subject, text_content, settings.EMAIL_HOST_USER, self.email)
#     email.attach_alternative(html_content, "text/html")
#     return email.send(fail_silently=False)
```
- **Trigger/Event**: N/A (commented; not in use)
- **Template**: N/A
- **Status**: Not active

---

## Email Templates Present
- `templates/layouts/base_mail.html` (base layout)
- `templates/mails/activate_email_form.html`
- `templates/mails/reset_password_form.html`
- `templates/mails/approved_form.html`
- `templates/mails/available_mail_form.html`
- `templates/mails/message_mail_form.html`
- `templates/mails/bootser_choose_mail_form.html`

All referenced templates exist.

---

## Summary by Model/Event
- **Account Activation**: `send_activation_code` → `activate_email_form.html`
- **Password Reset**: `reset_password` → `reset_password_form.html`
- **Booster Approved**: `booster_added_message` → `approved_form.html`
- **Available to Play**: `send_available_to_play_mail` → `available_mail_form.html`
- **New Chat Message**: `chat.signals: Message post_save` → `send_message_mail` → `message_mail_form.html`
- **Booster Assigned/Chosen**: `send_mail_bootser_choose` → `bootser_choose_mail_form.html`
- **Manual Test**: `accounts.views.test_email_view` (no template)

---

## Configuration Notes
- Ensure `settings.EMAIL_HOST_USER` and email backend settings are configured in `gameBoosterss/settings.py`.
- All sending functions use `EmailMultiAlternatives(..., settings.EMAIL_HOST_USER, ...)` and `fail_silently=False` to surface errors.


