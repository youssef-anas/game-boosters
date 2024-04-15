from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from accounts.models import BaseUser
# from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth import get_user_model
from datetime import date, timedelta
BaseUser = get_user_model()


class Registeration(UserCreationForm):
    class Meta:
        model = BaseUser
        fields = ("first_name","last_name","email","username","password1","password2",'country','profile_image')
        # fields = '__all__'

    def clean_email(self):
            email = self.cleaned_data['email']
            if self.instance.email == email:
                return email  
            if BaseUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email Already Exists.")
            return email

    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(),help_text="")
    password2 = forms.CharField(label="Password Confirmation",widget=forms.PasswordInput(),help_text="")
    username = forms.CharField(help_text="")

class EmailEditForm(forms.Form):
    old_email = forms.EmailField(label="Current Email")
    new_email = forms.EmailField(label="New Email")
    confirm_new_email = forms.EmailField(label="Confirm New Email")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Set placeholders and classes for each field
        self.fields['old_email'].widget.attrs.update({
            'placeholder': 'Old email',
            'class': 'form-control'
        })
        self.fields['new_email'].widget.attrs.update({
            'placeholder': 'New email',
            'class': 'form-control'
        })
        self.fields['confirm_new_email'].widget.attrs.update({
            'placeholder': 'Confirm new email',
            'class': 'form-control'
        })

    def clean_old_email(self):
        old_email = self.cleaned_data['old_email']
        if old_email != self.user.email:
            raise ValidationError("Current email does not match your existing email.")
        return old_email

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email']
        if BaseUser.objects.filter(email=new_email).exclude(pk=self.user.pk).exists():
            raise ValidationError("New email already exists.")
        return new_email

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get('new_email')
        confirm_new_email = cleaned_data.get('confirm_new_email')
        
        # Ensure new email matches the confirmation email
        if new_email and confirm_new_email and new_email != confirm_new_email:
            raise ValidationError("New email and confirmation email do not match.")
        
        return cleaned_data

    def save(self):
        self.user.email = self.cleaned_data['new_email']
        self.user.save()
        return self.user
    
class PasswordEditForm(PasswordChangeForm, SetPasswordForm):
    class Meta:
        model = BaseUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders and multiple classes for each field
        for field_name, field in self.fields.items():
            if field_name == 'new_password1':
                field.widget.attrs.update({
                    'placeholder': 'New Password',
                    'class': 'form-control'
                })
            elif field_name == 'new_password2':
                field.widget.attrs.update({
                    'placeholder': 'Confirm New Password',
                    'class': 'form-control'
                })
            else:
                field.widget.attrs.update({
                    'placeholder': field.label,
                    'class': 'form-control' 
                })
            field.label = ''

        self.fields['new_password1'].help_text = ''

class ProfileEditForm(UserChangeForm):
    # Define fields as day, month, and year inputs
    birth_day = forms.IntegerField(
        label="Day",
        min_value=1,
        max_value=31,
        required=False,
    )
    birth_month = forms.IntegerField(
        label="Month",
        min_value=1,
        max_value=12,
        required=False,
    )
    birth_year = forms.IntegerField(
        label="Year",
        required=False,
    )
    
    class Meta:
        model = BaseUser
        fields = ("username", "country", "birth_day", "birth_month", "birth_year")

    def clean(self):
        cleaned_data = super().clean()
        
        # Get the inputs for day, month, and year
        day = cleaned_data.get('birth_day')
        month = cleaned_data.get('birth_month')
        year = cleaned_data.get('birth_year')
        
        # Validate date of birth and convert it to a date object
        if day and month and year:

            try:
                birth_date = date(year, month, day)
                # Calculate the minimum allowed date of birth (18 years before today)
                min_birth_date = date.today() - timedelta(days=18*365)

                # Check if the date of birth is less than 18 years from today
                if birth_date > date.today():
                    raise ValidationError("Date of birth cannot be in the future.")
                elif birth_date > min_birth_date:
                    raise ValidationError("You must be at least 18 years old.")
                
                # If the date is valid, store it in the cleaned data
                self.cleaned_data['date_of_birth'] = birth_date
                
            except ValueError:
                raise ValidationError("Invalid date of birth.")
        
        # Raise an error if only some date parts were provided
        elif any([day, month, year]) and not all([day, month, year]):
            raise ValidationError("All fields (day, month, and year) must be filled out for date of birth.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Update date of birth if all fields are filled
        if 'date_of_birth' in self.cleaned_data:
            user.date_of_birth = self.cleaned_data['date_of_birth']
        
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Remove the password field
        self.fields.pop('password', None)
        self.fields['username'].help_text = ''

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Chat name',
            'class': 'form-control'  # Add your class here
        })
        self.fields['country'].widget.attrs.update({
            'placeholder': 'Chat country',
        })
        self.fields['birth_day'].widget.attrs.update({
            'placeholder': 'DD',
            'class': 'form-control datepicker-day'  # Add your class here
        })
        self.fields['birth_month'].widget.attrs.update({
            'placeholder': 'MM',
            'class': 'form-control datepicker-month'  # Add your class here
        })
        self.fields['birth_year'].widget.attrs.update({
            'placeholder': 'YYYY',
            'class': 'form-control datepicker-year'  # Add your class here
        })
    
