from django import forms
# from accounts.models import BaseUser
# from booster.models import Booster
from django import forms
from booster.models import WorkWithUs, Photo, Language
from django.core.exceptions import ValidationError

"""

Work with us model

nickname -> text
email -> email
Dicord_id -> text
language -> meny 
--------
game -> meny
rank --> text
server --> text
--------
check how meny game in game field
open field with every game that booster choose
upload pic 
"""


class WorkWithUsLevel1Form(forms.ModelForm):

    class Meta:
        model = WorkWithUs
        fields = ['nickname', 'email', 'discord_id', 'languages']
        widgets = {
            'languages': forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple custom-input', 'placeholder': 'Choose your language)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add classes and placeholders to each field
        self.fields['nickname'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Nickname'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Email'
        })
        self.fields['discord_id'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Discord ID'
        })
        # self.fields['languages'].widget.attrs.update({
        #     'class': 'form-control custom-input',
        #     'placeholder': 'e.g., English, Spanish, French'
        # })

        # Add help text for the 'languages' field
        self.fields['languages'].help_text = 'Enter the languages you are proficient in, separated by commas (e.g., English, Spanish, French).'
        

class WorkWithUsLevel2Form(forms.ModelForm):
    class Meta:
        model = WorkWithUs
        fields = ['game', 'rank', 'server']


class WorkWithUsLevel2Form(forms.ModelForm):
    class Meta:
        model = WorkWithUs
        fields = ['game', 'rank', 'server']
        widgets = {
            'game': forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple custom-input', 'placeholder': 'Choose your game)'}),
            'rank': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Rank'}),
            'server': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Server'}),
        }


class WorkWithUsLevel3Form(forms.ModelForm):
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)

    class Meta:
        model = Photo
        fields = ['image']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image2 = cleaned_data.get('image2')
        image3 = cleaned_data.get('image3')

        if not (image or image2 or image3):
            print("At least one image is required.")
            raise forms.ValidationError("At least one image is required.")        
        return cleaned_data

    
class WorkWithUsForm(forms.ModelForm):
    agree_privacy = forms.BooleanField(required=True)

    class Meta:
        model = WorkWithUs
        fields = '__all__'

    def create(self, commit=True, **kwargs):
        # Exclude many-to-many fields from cleaned_data
        m2m_fields = ['game', 'languages']  # Include 'languages' here
        m2m_data = {field: self.cleaned_data.pop(field) for field in m2m_fields if field in self.cleaned_data}

        obj = WorkWithUs.objects.create(**self.cleaned_data, **kwargs)

        for field, values in m2m_data.items():
            if field == 'languages':
                # Retrieve Language objects based on their primary keys
                languages = Language.objects.filter(pk__in=values)
                getattr(obj, field).set(languages)
            else:
                getattr(obj, field).set(values)

        return obj


class WorkWithUsLevel4Form(forms.ModelForm):
    agree_privacy = forms.BooleanField(required=True)

    class Meta:
        model = WorkWithUs
        fields = ['about_you', 'country', 'agree_privacy']
        widgets = {
            'about_you': forms.Textarea(attrs={'rows': 8, 'placeholder': 'About you', 'class': 'form-control custom-input'}),
        }