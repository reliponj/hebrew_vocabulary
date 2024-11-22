from django.contrib import admin

from binyan.models import BinyanInApp


@admin.register(BinyanInApp)
class BinyanInAppAdmin(admin.ModelAdmin):
    list_display = ['binyan', 'text_ru', 'text_ua', 'text_en', 'sort']
    list_editable = ['sort']
