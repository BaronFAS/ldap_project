from django.contrib.auth.admin import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    fieldsets = ((None, {"fields": ("name", "short_name", "domain_url", "password_reset_uri",)}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "short_name", "domain_url", "password_reset_uri",),
            },
        ),
    )
    search_fields = ["name"]
    ordering = ["name"]
    filter_horizontal = ()
