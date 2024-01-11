from django.contrib import admin

# Register your models here.

from wildRift.models import WildRiftTier, WildRiftRank, WildRiftMark, WildRiftPlacement, WildRiftDivisionOrder
admin.site.register(WildRiftRank)
admin.site.register(WildRiftTier)
admin.site.register(WildRiftMark)
admin.site.register(WildRiftPlacement)
admin.site.register(WildRiftDivisionOrder)