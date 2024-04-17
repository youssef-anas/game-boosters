from django.contrib import admin
from booster.models import OrderRating, Booster, WorkWithUs, Photo, BoosterPortfolio
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from gameBoosterss.utils import upload_image_to_firebase


admin.site.register(OrderRating)
admin.site.register(Photo)
admin.site.register(BoosterPortfolio)

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

        # Check if a profile image file is provided
        if profile_image_file:
            # Only upload image to Firebase if a file is provided
            profile_image_url = upload_image_to_firebase(profile_image_file,'booster/'+profile_image_file.name)
            instance.profile_image_url = profile_image_url
        if commit:
            instance.save()
        return instance
    
@admin.register(Booster)
class YourModelAdmin(admin.ModelAdmin):
    form = BoosterAdminForm    
