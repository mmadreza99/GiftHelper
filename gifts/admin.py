from django.contrib import admin
from django.utils.html import format_html

from .models import GiftList, GiftItem, Reservation


class GiftItemInline(admin.TabularInline):
    model = GiftItem
    extra = 1  # تعداد آیتم‌های اضافه برای ورود سریع


@admin.register(GiftList)
class GiftListAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')  # فیلتر براساس وضعیت عمومی و تاریخ ایجاد
    search_fields = ('title', 'user__username')
    inlines = [GiftItemInline]


@admin.register(GiftItem)
class GiftItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'gift_list', 'price', 'reserved')
    list_filter = ('reserved',)
    search_fields = ('name', 'gift_list__title')

    def mark_reserved(self, request, queryset):
        queryset.update(reserved=True)
    mark_reserved.short_description = "Mark selected items as reserved"

    def mark_unreserved(self, request, queryset):
        queryset.update(reserved=False)
    mark_unreserved.short_description = "Mark selected items as unreserved"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('item', 'reserved_by', 'reserved_at')
    search_fields = ('item__name', 'reserved_by__username')
    readonly_fields = ('reserved_at',)

    def item_link(self, obj):
        return format_html('<a href="/admin/app_name/giftitem/{}/">{}</a>', obj.item.id, obj.item.name)

    item_link.short_description = 'Gift Item'