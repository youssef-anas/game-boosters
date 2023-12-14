from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import BaseUser
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model

BaseUser = get_user_model()


class Registeration(UserCreationForm):
    phone_number = PhoneNumberField(label='Phone name', required=False)
    image = forms.ImageField(label='Profile Picture',  required=False)

    class Meta:
        model = BaseUser
        fields = ("first_name","last_name","email","username","password1","password2","image",'country', 'about_you')
        # fields = '__all__'

    def clean_email(self):
            email = self.cleaned_data['email']
            if self.instance.email == email:
                return email  
            if BaseUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email Already Exists.")
            return email

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        help_text=""
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(),
        help_text=""
    )
    username = forms.CharField(
        help_text=""
    )