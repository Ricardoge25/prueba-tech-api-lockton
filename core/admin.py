
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Menu

User = get_user_model()


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
  list_display = ("id", "name", "route", "is_active")
  list_display_links = ("name",)
  list_filter = ("is_active",)
  search_fields = ("name", "route", "description")
  ordering = ("name",)


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
  list_display = (
    "id",
    "username",
    "email",
    "first_name",
    "last_name",
    "is_staff",
    "is_active",
  )
  list_filter = ("is_staff", "is_active")
  search_fields = ("username", "email", "first_name", "last_name")
  ordering = ("username",)
