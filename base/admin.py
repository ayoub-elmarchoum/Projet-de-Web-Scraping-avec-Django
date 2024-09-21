from django.contrib import admin
from .models import ScrapedData, CustomUser, Newsletter, UserProfile

from django.contrib.auth import get_user_model

# Register your models here.


admin.site.register(ScrapedData)
admin.site.register(CustomUser)
admin.site.register(Newsletter)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','profile_picture')
    

admin.site.register(UserProfile, UserProfileAdmin)