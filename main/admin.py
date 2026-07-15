from django.contrib import admin

from .models import (
    Booking,
    ContactMessage,
    MenuCategory,
    MenuItem,
    PrivateEvent,
    Speciality,
    StaticSection,
    UserProfile,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "user")
    search_fields = ("full_name", "phone", "user__email")


@admin.register(StaticSection)
class StaticSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("title", "subtitle", "text")


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "order")
    list_editable = ("is_active", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "on_main", "is_active", "order")
    list_filter = ("category", "on_main", "is_active")
    list_editable = ("price", "on_main", "is_active", "order")
    search_fields = ("title", "subtitle")


@admin.register(PrivateEvent)
class PrivateEventAdmin(admin.ModelAdmin):
    list_display = ("title", "position", "is_active", "order")
    list_editable = ("position", "is_active", "order")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "time", "people", "email", "phone", "created_at")
    list_filter = ("date", "created_at")
    search_fields = ("name", "email", "phone")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
