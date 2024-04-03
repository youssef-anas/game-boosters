from django import forms
from accounts.models import BaseUser
from django.contrib.auth.forms import SetPasswordForm


class EmailForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not BaseUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not associated with any user.")
        return email

class ResetCodeForm(forms.Form):
    reset_code = forms.IntegerField(max_value=99999, label='Reset Code', widget= forms.NumberInput)


class PasswordChangeCustomForm(SetPasswordForm):
    pass


