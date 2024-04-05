from django import forms
# from accounts.models import BaseUser
# from booster.models import Booster
from django import forms
from booster.models import WorkWithUs, Photo


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

class WorkWithUsLevel2Form(forms.ModelForm):
    class Meta:
        model = WorkWithUs
        fields = ['game', 'rank', 'server']
        widgets = {
            'game': forms.SelectMultiple,
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
            raise forms.ValidationError("At least one image is required.")        
        return cleaned_data
    
    
class WorkWithUsForm(forms.ModelForm):
    class Meta:
        model = WorkWithUs
        fields = '__all__'

    def create(self, commit=True, **kwargs):
        # Exclude many-to-many fields from cleaned_data
        m2m_fields = ['game']
        m2m_data = {field: self.cleaned_data.pop(field) for field in m2m_fields if field in self.cleaned_data}

        obj = WorkWithUs.objects.create(**self.cleaned_data, **kwargs)

        for field, values in m2m_data.items():
            getattr(obj, field).set(values)
        return obj