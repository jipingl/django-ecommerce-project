from django.contrib import admin

from account.models import UserBase


class UserBaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserBase, UserBaseAdmin)
