# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives

# class MadboostEmailSender:
        
#     def __init__(self, subject: str, email: str | list, template_name: str, context: dict) -> None:
#         if not subject or not email or not template_name or not context:
#             raise ValueError("All arguments must be provided.")
#         self.subject = subject
#         self.email = email if isinstance(email, list) else [email]
#         self.template_name = template_name
#         self.context = context
        
#     def send_mail(self) -> int:
#         html_content = render_to_string(self.template_name, self.context)
#         text_content = strip_tags(html_content)
#         email = EmailMultiAlternatives(self.subject, text_content, settings.EMAIL_HOST_USER, self.email)
#         email.attach_alternative(html_content, "text/html")
#         return email.send(fail_silently=False)
