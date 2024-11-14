from django.contrib import admin
from django.urls import reverse
from booster.models import OrderRating, Booster, WorkWithUs, Photo, BoosterPortfolio, CreateBooster, Language, BoosterRank
from accounts.models import Wallet
from django.utils.safestring import mark_safe
from django.forms import ModelForm, ValidationError
from gameBoosterss.utils import upload_image_to_firebase
from django import forms
from accounts.models import BaseUser
from gameBoosterss.utils import booster_added_message
from faker import Faker
from django.shortcuts import redirect
from accounts.admin import NoDeleteAdmin, NoDeleteEditAdmin
from django.utils.html import format_html
from django.db.models import Q
faker = Faker()


admin.site.register(OrderRating, NoDeleteAdmin)
# admin.site.register(Photo)

class BoosterPortfolioAdmin(admin.ModelAdmin):
    list_filter = ('approved',)
    list_display = ('booster', 'open_img_link', 'approved')

    def open_img_link(self, obj):
        print(obj.get_image_url)
        return format_html(f'<a href="{obj.get_image_url()}" target="_blank">View Image</a>')
    open_img_link.short_description = 'Image'
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
    
class HasMoneyFilter(admin.SimpleListFilter):
    title = 'Has Money'  # The label that appears for the filter
    parameter_name = 'has_money'  # The URL parameter name for the filter

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(booster__wallet__money__gt=0)  # Assuming 'booster' is related to 'Wallet'
        if self.value() == 'no':
            return queryset.filter(booster__wallet__money__lte=0)
        return queryset    
    
@admin.register(Booster)
class YourModelAdmin(admin.ModelAdmin):
    form = BoosterAdminForm
    list_display = ['booster_username', 'games_list', 'money']
    list_filter = [HasMoneyFilter, 'games']
    search_fields = ['booster__username']

    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        (None, {'fields': ('games', 'paypal_account', 'discord_id', 'can_choose_me')}),
        ('Personal info', {'fields': ('languages', 'about_you', 'profile_image')}),
        ('played Games', {'fields': ('is_wr_player', 'is_valo_player', 'is_pubg_player','is_lol_player','is_tft_player','is_wow_player', 'is_hearthstone_player', 'is_mobleg_player', 'is_rl_player', 'is_dota2_player', 'is_hok_player', 'is_overwatch2_player', 'is_csgo2_player')}),
        ('Ranks', {'fields': ('achived_rank_wr', 'achived_rank_valo', 'achived_rank_pubg', 'achived_rank_lol', 'achived_rank_tft', 'achived_rank_wow', 'achived_rank_hearthstone', 'achived_rank_mobleg', 'achived_rank_rl', 'achived_rank_dota2', 'achived_rank_hok', 'achived_rank_overwatch2', 'achived_rank_csgo2')}),
    )
    def booster_username(self, obj):
        return obj.booster.username
    booster_username.short_description = 'Name'

    def games_list(self, obj):
        return ", ".join([game.link for game in obj.games.all()])  # Assuming `games` is a many-to-many field
    games_list.short_description = 'Games'

    def money(self, obj):
        wallet, created = Wallet.objects.get_or_create(user=obj.booster)
        transaction_url = reverse('admin:accounts_transaction_add')
        return format_html(
            '<a href="{}?user={}&amount={}" target="_blank">{}</a>',
            transaction_url,
            obj.booster.id,  # Pass the booster ID as a GET parameter to pre-select the user
            wallet.money,  # Pass the amount as a GET parameter to pre-fill the transaction amount
            round(wallet.money, 2)  # Display the rounded money amount as the clickable text
        )
    money.short_description = 'Money'

    

class CreateBoosterForm(forms.ModelForm):
    class Meta:
        model = CreateBooster
        fields = '__all__'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if BaseUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if BaseUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        # Example extra validation: Ensure at least one game type is selected
        game_fields = [
            'is_wr_player', 'is_valo_player', 'is_pubg_player', 'is_lol_player',
            'is_tft_player', 'is_wow_player', 'is_hearthstone_player', 
            'is_mobleg_player', 'is_rl_player', 'is_dota2_player', 
            'is_hok_player', 'is_overwatch2_player', 'is_csgo2_player'
        ]
        if not any(cleaned_data.get(field) for field in game_fields):
            raise forms.ValidationError("At least one game type must be selected.")

        # Additional custom validations can be added here

        return cleaned_data

    def save(self, commit=True):
        # Continue with the save logic without additional checks here
        fake_password = faker.password(length=12)
        email = self.cleaned_data.pop('email')
        username = self.cleaned_data.pop('username')
        instance = super().save(commit=False)

        try:
            user = BaseUser.objects.create_user(username=username, email=email, password=fake_password, is_booster=True)
            user.set_password(fake_password)
            user.save()

            booster = Booster.objects.create(booster=user, **self.cleaned_data)

            if commit:
                instance.delete()

            booster_added_message(email, fake_password, username)
            return booster

        except Exception as e:
            # Handle unexpected errors gracefully
            self.add_error(None, f"An unexpected error occurred: {e}")
            return None


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