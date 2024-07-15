from django.contrib import admin
from django.contrib.auth.models import Group

from user.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_subscribe', 'sub_date']
