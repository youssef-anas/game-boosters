from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model
from booster.models import Booster, BoosterRank
from wildRift.models import WildRiftRank
from valorant.models import ValorantRank
from pubg.models import PubgRank
from leagueOfLegends.models import LeagueOfLegendsRank
from tft.models import TFTRank
from hearthstone.models import HearthstoneRank
from rocketLeague.models import RocketLeagueRank
from mobileLegends.models import MobileLegendsRank
from WorldOfWarcraft.models import WorldOfWarcraftRank
from overwatch2.models import Overwatch2Rank
from dota2.models import Dota2Rank
from csgo2.models import Csgo2Rank
from honorOfKings.models import HonorOfKingsRank
from booster.models import Language
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
BaseUser = get_user_model()

# class Registeration_Booster(UserCreationForm):
#     image = forms.ImageField(label='Profile Picture', required=False)
#     class Meta:
#         model = BaseUser
#         fields = ("email", "username", 'image', 'country')
#         # fields = '__all__'

#     def clean_email(self):
#             email = self.cleaned_data['email']
#             if self.instance.email == email:
#                 return email  
#             if BaseUser.objects.filter(email=email).exists():
#                 raise forms.ValidationError("Email Already Exists.")
#             return email
    
#     password1 = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(),
#         help_text=""
#     )
#     password2 = forms.CharField(
#         label="Password Confirmation",
#         widget=forms.PasswordInput(),
#         help_text=""
#     )
#     username = forms.CharField(
#         help_text=""
#     )
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_active = False
#         # user.is_booster = True
#         if commit:
#             user.save()
#         return user
    
class ProfileEditForm(UserChangeForm, forms.ModelForm):
    full_name = forms.CharField(max_length=300, 
    widget=forms.TextInput(attrs={'placeholder': 'Enter full name', 'class': 'form-control custom-input'}),
    label='Name', required=False)

    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput())
    about_you = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'About you', 'class': 'form-control custom-input'}), 
        label='Bio',
        required=False)

    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple custom-input'}), label='Languages you know')

    
    # Define form fields for achived ranks
    achived_rank_wr = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=1), required=False, label='Lol: Wild Rift')

    achived_rank_valo = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=2), required=False, label='VALORANT')

    achived_rank_pubg = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=3), required=False, label='Pubg Mobile')

    achived_rank_lol = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=4), required=False, label='League of Legends')

    achived_rank_tft = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=5), required=False, label='Team Fight Tactics')

    achived_rank_wow = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=6), required=False, label='World of Warcraft')

    achived_rank_hearthstone = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=7), required=False, label='Hearthstone')

    achived_rank_mobleg = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=8), required=False, label='Mobile Legends')

    achived_rank_rl = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=9), required=False, label='Rocket League')

    achived_rank_dota2 = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=10), required=False, label='Dota 2')

    achived_rank_hok = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=11), required=False, label='Honer Of King')

    achived_rank_overwatch2 = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=12), required=False, label='Overwatch 2')

    achived_rank_csgo2 = forms.ModelChoiceField(queryset=BoosterRank.objects.filter(game__pk=13), required=False, label='CS GO 2')

    class Meta:
        model = BaseUser
        fields = []

    class MetaBooster:
        model = Booster
        fields = [
            'profile_image',
            'about_you',
            'achived_rank_wr',
            'achived_rank_valo',
            'achived_rank_pubg',
            'achived_rank_lol',
            'achived_rank_tft',
            'achived_rank_wow',
            'achived_rank_hearthstone',
            'achived_rank_mobleg',
            'achived_rank_rl',
            'achived_rank_dota2',
            'achived_rank_hok',
            'achived_rank_overwatch2',
            'achived_rank_csgo2',
            'languages'
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

        if 'languages' in self.fields:
            # Get the languages associated with the user
            user_languages = self.instance.booster.languages.all()
            self.initial['languages'] = user_languages

        
        # Get the Booster instance associated with the user
        booster = None
        if hasattr(self.instance, 'booster'):
            booster = self.instance.booster

        if hasattr(self.instance, 'first_name') and hasattr(self.instance, 'last_name'):
            # Combine first name and last name for the full_name field
            full_name = f"{self.instance.first_name} {self.instance.last_name}"
            self.initial['full_name'] = full_name
        
        # Set the initial value for about_you field from the Booster instance
        if booster and hasattr(booster, 'about_you'):
            self.initial['about_you'] = booster.about_you

        # should_include_languages = True  # Set your condition here

        # if should_include_languages:
        #     if 'languages' not in self.fields:
        #         self.fields['languages'] = forms.CharField(
        #             max_length=300, 
        #             widget=forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Languages'}),
        #             label='Languages',
        #             required=False
        #         )
        #     # If you have a Booster instance, populate the initial data for languages
        #     if hasattr(self.instance, 'booster') and self.instance.booster:
        #         booster = self.instance.booster
        #         if booster.languages:
        #             self.initial['languages'] = ', '.join(booster.languages)
        # else:
        #     # Remove the languages field if it exists
        #     self.fields.pop('languages', None)
        
        # Define mapping from boolean flags to rank fields
        mapping = {
            'is_wr_player': 'achived_rank_wr',
            'is_valo_player': 'achived_rank_valo',
            'is_pubg_player': 'achived_rank_pubg',
            'is_lol_player': 'achived_rank_lol',
            'is_tft_player': 'achived_rank_tft',
            'is_wow_player': 'achived_rank_wow',
            'is_hearthstone_player': 'achived_rank_hearthstone',
            'is_mobleg_player': 'achived_rank_mobleg',
            'is_rl_player': 'achived_rank_rl',
            'is_dota2_player': 'achived_rank_dota2',
            'is_hok_player': 'achived_rank_hok',
            'is_overwatch2_player': 'achived_rank_overwatch2',
            'is_csgo2_player': 'achived_rank_csgo2',
        }
        
        # If the booster instance exists, iterate over the mapping and remove achived rank fields if the corresponding boolean flag is False
        if booster:
            for bool_field, rank_field in mapping.items():
                if not getattr(booster, bool_field, False):
                    self.fields.pop(rank_field, None)

                if hasattr(booster, rank_field):
                    self.initial[rank_field] = getattr(booster, rank_field)
                
        # Remove password field if it exists
        self.fields.pop('password', None)
        self.fields.pop('last_name', None)
        self.fields.pop('last_name', None)
        self.fields.pop('username', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Update user full name
        if 'full_name' in self.cleaned_data:
            full_name = self.cleaned_data['full_name']
            user.set_full_name(full_name)


        # Create a dictionary with the fields related to the Booster model
        booster_data = {
            'about_you': self.cleaned_data.get('about_you'),
            'achived_rank_wr': self.cleaned_data.get('achived_rank_wr'),
            'achived_rank_valo': self.cleaned_data.get('achived_rank_valo'),
            'achived_rank_pubg': self.cleaned_data.get('achived_rank_pubg'),
            'achived_rank_lol': self.cleaned_data.get('achived_rank_lol'),
            'achived_rank_tft': self.cleaned_data.get('achived_rank_tft'),
            'achived_rank_wow': self.cleaned_data.get('achived_rank_wow'),
            'achived_rank_hearthstone': self.cleaned_data.get('achived_rank_hearthstone'),
            'achived_rank_mobleg': self.cleaned_data.get('achived_rank_mobleg'),
            'achived_rank_rl': self.cleaned_data.get('achived_rank_rl'),
            'achived_rank_dota2': self.cleaned_data.get('achived_rank_dota2'),
            'achived_rank_hok': self.cleaned_data.get('achived_rank_hok'),
            'achived_rank_overwatch2': self.cleaned_data.get('achived_rank_overwatch2'),
            'achived_rank_csgo2': self.cleaned_data.get('achived_rank_csgo2'),
        }
        
        # Get or create the Booster instance for the user
        booster_instance, created = Booster.objects.get_or_create(booster=user)

        # Update booster data
        if not created:
            for key, value in booster_data.items():
                if value is not None:
                    setattr(booster_instance, key, value)
            booster_instance.save()
        else:
            Booster.objects.create(booster=user, **booster_data)

        # if 'languages' in self.cleaned_data:
        #     languages_data = self.cleaned_data['languages']
        #     booster_instance.languages = languages_data.split(', ')

        if 'languages' in self.cleaned_data:
            languages_data = self.cleaned_data['languages']
            booster_instance.languages.set(languages_data)
        
        booster_instance.save()

        # Save the user if commit is True
        if commit:
            user.save()
        
        return user

class PayPalEmailEditForm(forms.Form):
    paypal_account = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Paypal email','class': 'form-control custom-input'}),
        help_text='To confirm ur changes write your current password and press save:',
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control custom-input'}))
    

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        # Authenticate the user with the provided password
        user = authenticate(username=self.user.username, password=password)
        if not user:
            raise ValidationError('Incorrect password. Please try again.')

        return cleaned_data

    def save(self):
        # Save the new PayPal email
        self.user.booster.paypal_account = self.cleaned_data['paypal_account']
        self.user.booster.save()

class PasswordEditForm(PasswordChangeForm, SetPasswordForm):
    class Meta:
        model = BaseUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'new_password1':
                field.widget.attrs.update({
                    'placeholder': 'New Password',
                    'class': 'form-control custom-input'
                })
            elif field_name == 'new_password2':
                field.widget.attrs.update({
                    'placeholder': 'Confirm New Password',
                    'class': 'form-control custom-input'
                })
            else:
                field.widget.attrs.update({
                    'placeholder': field.label,
                    'class': 'form-control custom-input' 
                })
            field.label = ''

        self.fields['new_password1'].help_text = ''
        
        # Ensuring no field has the autofocus attribute
        for field in self.fields.values():
            if 'autofocus' in field.widget.attrs:
                del field.widget.attrs['autofocus']