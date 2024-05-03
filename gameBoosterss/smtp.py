from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings

class CustomEmailSender:
    def __init__(self):
        self.smtp_settings = {
            'host': settings.EMAIL_HOST,
            'port': settings.EMAIL_PORT,
            'username': settings.DEFAULT_FROM_EMAIL,
            'password': settings.EMAIL_HOST_PASSWORD,
            'use_tls': settings.EMAIL_USE_TLS,
            'use_ssl': not settings.EMAIL_USE_TLS
        }

    def send_email(self, subject, message, sender_email, recipient_email):
        email = EmailMessage(subject, message, sender_email, [recipient_email])
        email.connection = EmailBackend(**self.smtp_settings)
        try:
            email.send()
            print('Email sent successfully!')
        except Exception as e:
            print(f'Failed to send email: {e}')

# Example usage
if __name__ == "__main__":
    email_sender = CustomEmailSender()
    subject = 'Test Email'
    message = 'Hello there! This is a test email from your Django app.'
    sender_email = 'customerservice@madboost.gg'
    recipient_email = 'shethr999@gmail.com'

    # Send email
    email_sender.send_email(subject, message, sender_email, recipient_email)
