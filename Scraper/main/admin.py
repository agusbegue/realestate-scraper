from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import ScrapyJob, Property, Statistics, User

admin.site.register(ScrapyJob)
admin.site.register(Property)
admin.site.register(Statistics)

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)





