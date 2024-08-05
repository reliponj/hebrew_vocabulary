from django.contrib import admin
from django.shortcuts import redirect

from ivrit.management.commands.import_kluch_v2 import save_all_kluch
from ivrit.models import Root, Vocabulary, Spisok6, RCategory, Spisok1, Setting, Kluch


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        settings = Setting.get_settings()
        return redirect(request.path + f'{settings.id}/')


@admin.register(Kluch)
class KluchAdmin(admin.ModelAdmin):
    list_display = ['value', 'value_ru', 'value_ua', 'value_en']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        save_all_kluch()


@admin.register(Vocabulary)
class Vocabulary6Admin(admin.ModelAdmin):
    list_display = ['root', 'link', 'binyan', 'word', 'word_u', 'word_a', 'words1', 'words2', 'words', 'words_clear']
    search_fields = ['root', 'word', 'word_u', 'word_a', 'words1', 'words2', 'words', 'words_clear']


@admin.register(Spisok6)
class Spisok6Admin(admin.ModelAdmin):
    list_display = ['roots', 'words', 'tables', 'tables_2']
    search_fields = ['roots', 'words']


@admin.register(Spisok1)
class Spisok1Admin(admin.ModelAdmin):
    list_display = ['roots', 'words', 'word', 'r', 'links']
    search_fields = ['roots', 'words', 'word']


# class BinyanAdmin(admin.TabularInline):
#     model = Binyan
#     extra = 0
#
#
# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ['group']
#
#
# @admin.register(Root)
# class RootAdmin(admin.ModelAdmin):
#     search_fields = ['root']
#     list_display = ['root', 'get_binyans', 'get_groups', 'number']
#     inlines = [BinyanAdmin]


@admin.register(RCategory)
class RCategoryAdmin(admin.ModelAdmin):
    list_display = ['r', 'description']
