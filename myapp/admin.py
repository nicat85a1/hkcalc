# myapp/admin.py

from django.contrib import admin
from .models import CoinData, UserProfile

class CoinDataAdmin(admin.ModelAdmin):
    list_display = ('coin_name', 'sbk_value', 'price', 'is_default')
    list_filter = ('is_default',)

admin.site.register(CoinData, CoinDataAdmin)

admin.site.register(UserProfile)