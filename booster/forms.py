from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model
BaseUser = get_user_model()


class Registeration_Booster(UserCreationForm):
    phone_number = PhoneNumberField(label='Phone name', required=False)
    image = forms.ImageField(label='Profile Picture',  required=False)

    class Meta:
        model = BaseUser
        fields = ("email", "username", "image", 'country', 'about_you', 'achived_rank')
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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        # user.is_booster = True
        if commit:
            user.save()
        return user
    
class ProfileEditForm(UserChangeForm):
    phone_number = PhoneNumberField(label='Phone number', required=False)
    image = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = BaseUser
        fields = ("email", "username", "image", 'country', 'about_you', 'achived_rank')

    def clean_email(self):
        email = self.cleaned_data['email']
        if BaseUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the password field from the form
        self.fields.pop('password', None)
    
    username = forms.CharField(
        help_text=""
    )

class PasswordEditForm(PasswordChangeForm, SetPasswordForm):
    class Meta:
        model = BaseUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = '' 