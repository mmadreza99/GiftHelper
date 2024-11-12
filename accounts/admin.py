from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'bio')  # نمایش فیلدهای کلیدی در لیست
    search_fields = ('user__username', 'nickname')  # قابلیت جستجو براساس یوزرنیم و نیک‌نیم

