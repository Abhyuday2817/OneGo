from django.contrib import admin
from .models import Badge, UserBadge


class UserBadgeInline(admin.TabularInline):
    """
    Shows all users who earned a badge in the Badge admin page.
    """
    model = UserBadge
    extra = 0
    fields = ("user", "awarded_at", "verified", "expires_at", "note")
    readonly_fields = ("user", "awarded_at", "expires_at")
    can_delete = False
    show_change_link = True


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "level", "expires_in_days", "icon_url")
    list_filter = ("level",)
    search_fields = ("name", "slug", "description")
    ordering = ("level", "name")
    inlines = [UserBadgeInline]
    readonly_fields = ("slug",)  # Optional: protect against editing slug

    fieldsets = (
        ("Basic Info", {
            "fields": ("slug", "name", "description", "level")
        }),
        ("Badge Icon & Rules", {
            "fields": ("icon_url", "expires_in_days")
        }),
    )


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "badge", "awarded_at", "verified", "expires_at", "is_active_display")
    list_filter = ("verified", "badge__level", "badge__name")
    search_fields = ("user__username", "badge__name", "note")
    ordering = ("-awarded_at",)
    autocomplete_fields = ("user", "badge")
    list_editable = ("verified",)
    readonly_fields = ("awarded_at", "expires_at", "is_active_display")

    def is_active_display(self, obj):
        return obj.is_active()
    is_active_display.short_description = "Active?"
    is_active_display.boolean = True
