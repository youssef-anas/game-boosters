from django.contrib import admin

# Register your models here.

from wildRift.models import WildRiftTier, WildRiftRank, WildRiftMark
admin.site.register(WildRiftRank)
admin.site.register(WildRiftTier)
admin.site.register(WildRiftMark)