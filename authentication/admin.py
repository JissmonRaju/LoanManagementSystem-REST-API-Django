from django.contrib import admin
from .models import UserOTP


class UserOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'is_still_valid')
    readonly_fields = ('user', 'otp', 'created_at', 'expires_at')

    def is_still_valid(self, obj):
        return not obj.has_expired()

    is_still_valid.boolean = True
    is_still_valid.short_description = "OTP Valid"


admin.site.register(UserOTP, UserOTPAdmin)
