from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model
BaseUser = get_user_model()


class Registeration_Booster(UserCreationForm):
    phone_number = PhoneNumberField(label='Phone name', required=False)
    image = forms.ImageField(label='Profile Picture',  required=False)

    class Meta:
        model = BaseUser
        fields = ("email", "username", "password1", "password2", "image", 'country', 'about_you')
        # fields = '__all__'

    def clean_email(self):
            email = self.cleaned_data['email']
            if self.instance.email == email:
                return email  
            if BaseUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email Already Exists.")
            return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user