from django.contrib import admin
from django.urls import reverse
from booster.models import OrderRating, Booster, WorkWithUs, Photo, BoosterPortfolio, CreateBooster, Language, BoosterRank
from django.utils.safestring import mark_safe
from django.forms import ModelForm, ValidationError
from gameBoosterss.utils import upload_image_to_firebase
from django import forms
from accounts.models import BaseUser
from gameBoosterss.utils import booster_added_message
from faker import Faker
from django.shortcuts import redirect
from accounts.admin import NoDeleteAdmin, NoDeleteEditAdmin

faker = Faker()


admin.site.register(OrderRating, NoDeleteAdmin)
# admin.site.register(Photo)

class BoosterPortfolioAdmin(admin.ModelAdmin):
    list_filter = ('approved',)
admin.site.register(BoosterPortfolio, BoosterPortfolioAdmin)

class BoosterRankAdmin(admin.ModelAdmin):
    list_filter = ('game',)

admin.site.register(BoosterRank, BoosterRankAdmin)

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['image_preview',] 
    readonly_fields = ['image_preview',]

    def image_preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="500" height="500">') if obj.image else '-'
    image_preview.short_description = 'Image Preview'

@admin.register(WorkWithUs)
class WorkWithUsAdmin(admin.ModelAdmin):
    inlines = [PhotoInline,]


class BoosterAdminForm(ModelForm):
    class Meta:
        model = Booster
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        profile_image_file = self.cleaned_data.get('profile_image')
        if profile_image_file:
            print(profile_image_file)
            try:
                profile_image_url = upload_image_to_firebase(profile_image_file, 'booster/' + profile_image_file.name)
                instance.profile_image = profile_image_url
            except Exception as e:
                error_message = f"Error uploading image to Firebase: {e}"
                print(error_message)
                # raise ValidationError({'profile_image': [error_message]})
        else:
            # If no image data is provided, handle the case accordingly
            error_message = "No image data provided"
            forms.ValidationError({'profile_image': [error_message]})
        if commit:
            instance.save()
        return instance
    
@admin.register(Booster)
class YourModelAdmin(admin.ModelAdmin):
    form = BoosterAdminForm
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        (None, {'fields': ('games', 'paypal_account', 'discord_id', 'can_choose_me')}),
        ('Personal info', {'fields': ('languages', 'about_you', 'profile_image')}),
        ('played Games', {'fields': ('is_wr_player', 'is_valo_player', 'is_pubg_player','is_lol_player','is_tft_player','is_wow_player', 'is_hearthstone_player', 'is_mobleg_player', 'is_rl_player', 'is_dota2_player', 'is_hok_player', 'is_overwatch2_player', 'is_csgo2_player')}),
        ('Ranks', {'fields': ('achived_rank_wr', 'achived_rank_valo', 'achived_rank_pubg', 'achived_rank_lol', 'achived_rank_tft', 'achived_rank_wow', 'achived_rank_hearthstone', 'achived_rank_mobleg', 'achived_rank_rl', 'achived_rank_dota2', 'achived_rank_hok', 'achived_rank_overwatch2', 'achived_rank_csgo2')}),
    )

class CreateBoosterForm(ModelForm):
    class Meta:
        model = CreateBooster
        fields = '__all__'

    def save(self, commit=True):
        user = None
        booster = None
        try:
            fake_password = faker.password(length=12) 
            email = self.cleaned_data.pop('email')
            username = self.cleaned_data.pop('username') 
            instance = super().save(commit=False)
            user = BaseUser.objects.create_user(username=username, email=email, password=fake_password, is_booster=True)
            user.set_password(fake_password)
            booster = Booster.objects.create(booster=user, **self.cleaned_data)
            if commit:
                instance.delete()  
            booster_added_message(email, fake_password, username)        
            return user  
        except Exception as e:
            if user:
                user.delete()
            if booster:
                booster.delete()
            raise forms.ValidationError("An error occurred while processing the form. Please try again later.")

@admin.register(CreateBooster)
class CreateBoosterAdmin(admin.ModelAdmin):
    form = CreateBoosterForm

    def changelist_view(self, request, extra_context=None):
        if request.path == reverse('admin:booster_createbooster_changelist'):
            return redirect('admin:booster_createbooster_add')
        return super().changelist_view(request, extra_context)
    
    fieldsets = (
        ('New Booster Info', {'fields': ('username', 'email')}),
        ('Booster Games', {
            'fields': (
                'is_wr_player', 'is_valo_player', 'is_pubg_player',
                'is_lol_player', 'is_tft_player', 'is_wow_player',
                'is_hearthstone_player', 'is_mobleg_player', 'is_rl_player',
                'is_dota2_player', 'is_hok_player', 'is_overwatch2_player',
                'is_csgo2_player',
            ),
        }),
        )
    
admin.site.register(Language)    