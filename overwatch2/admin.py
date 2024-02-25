from django.contrib import admin
from overwatch2.models import Overwatch2Rank, Overwatch2Tier, Overwatch2Mark, Overwatch2DivisionOrder

admin.site.register(Overwatch2Rank)
admin.site.register(Overwatch2Tier)
admin.site.register(Overwatch2Mark)
admin.site.register(Overwatch2DivisionOrder)