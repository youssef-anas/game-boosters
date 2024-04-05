from django.contrib import admin
from booster.models import OrderRating, Booster, WorkWithUs, Photo
from django.utils.safestring import mark_safe


admin.site.register(OrderRating)
admin.site.register(Booster)
admin.site.register(Photo)

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
