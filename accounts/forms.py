from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import BaseUser
from phonenumber_field.formfields import PhoneNumberField


class Registeration(UserCreationForm):
    phone_number = PhoneNumberField(label='Phone name', required=False)
    image = forms.ImageField(label='Profile Picture',  required=False)

    class Meta:
        model = BaseUser
        fields = ("first_name","last_name","email","username","password1","password2","image")
        # fields = '__all__'

    def clean_email(self):
            email = self.cleaned_data['email']
            if self.instance.email == email:
                return email  
            if BaseUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email Already Exists.")
            return email