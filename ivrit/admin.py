from django.contrib import admin
from django.shortcuts import redirect

from ivrit.models import Root, Vocabulary, Spisok6, RCategory, Spisok1, Binyan, Group, Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        settings = Setting.get_settings()
        return redirect(request.path + f'{settings.id}/')


@admin.register(Vocabulary)
class Vocabulary6Admin(admin.ModelAdmin):
    list_display = ['root', 'link', 'binyan', 'word', 'word_u', 'word_a', 'words1', 'words']


@admin.register(Spisok6)
class Spisok6Admin(admin.ModelAdmin):
    list_display = ['roots', 'words', 'tables', 'tables_2']


@admin.register(Spisok1)
class Spisok1Admin(admin.ModelAdmin):
    list_display = ['roots', 'words', 'word', 'r', 'links']


class BinyanAdmin(admin.TabularInline):
    model = Binyan
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group']


@admin.register(Root)
class RootAdmin(admin.ModelAdmin):
    search_fields = ['root']
    list_display = ['root', 'get_binyans', 'get_groups', 'number']
    inlines = [BinyanAdmin]


@admin.register(RCategory)
class RCategoryAdmin(admin.ModelAdmin):
    list_display = ['r', 'description']
