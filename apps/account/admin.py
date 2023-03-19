from django.contrib import admin

from apps.account.models import Account, UserProfile

admin.site.register(Account),
admin.site.register(UserProfile)