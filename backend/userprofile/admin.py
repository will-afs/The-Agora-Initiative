from django.contrib import admin

# Register your models here.

from userprofile.models import UserProfile

admin.site.register(UserProfile)

