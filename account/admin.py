# account/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from .models import CustomUser 



class CustomUserAdmin(BaseUserAdmin):
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (('Additional Info'), {'fields': ('profile_image',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (('Additional Info'), {'fields': ('profile_image',)}),
    )

    # اگر میخواهید لیست نمایش کاربران در ادمین تغییر کند
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_image')



admin.site.register(CustomUser,CustomUserAdmin)

