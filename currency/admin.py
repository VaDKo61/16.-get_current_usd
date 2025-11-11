from django.contrib import admin
from .models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('rate', 'timestamp')
    list_filter = ('timestamp', )
    ordering = ('-timestamp', )
