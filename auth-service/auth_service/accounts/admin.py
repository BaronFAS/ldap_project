import datetime as dt
import jwt

from django.contrib import admin
from django.urls import reverse
from django.urls import path
from django.utils.html import format_html

from external_services.models import Services
from accounts.forms import ServicesForm
from auth_service.config import (
    SECRET_KEY_SERVICE,
    JWT_TOKEN_EXTERNAL_SERVICES,
)


class ServicesAdmin(admin.ModelAdmin):
    """Allows you to create and update a custom
    jwt token for access to API external services."""
    form = ServicesForm
    list_display = (
        "service_name",
        "service_url",
        "jwt_token_display",
        "created_at",
        "updated_at",
        "regenerate_token_button"
    )
    readonly_fields = ("jwt_token", "created_at", "updated_at")

    def jwt_token_display(self, obj):
        return f"{obj.jwt_token[:50]}..."
    jwt_token_display.short_description = "JWT Token"

    def regenerate_token_button(self, obj):
        return format_html(
            '<a class="btn" href="{}">{}</a>',
            reverse("admin:services_regenerate_token", args=[obj.pk]),
            "Update token"
        )
    regenerate_token_button.short_description = "Update token"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:pk>/regenerate-token/",
                self.admin_site.admin_view(self.regenerate_token_view),
                name="services_regenerate_token"
            )
        ]
        return custom_urls + urls

    def regenerate_token_view(self, request, pk):
        obj = self.get_object(request, pk)
        exp_datetime = dt.datetime.utcnow() + dt.timedelta(
            days=JWT_TOKEN_EXTERNAL_SERVICES
        )
        payload = {
            "service_name": obj.service_name,
            "exp": exp_datetime,
            "iat": dt.datetime.utcnow(),
        }
        secret_key = SECRET_KEY_SERVICE
        obj.jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
        obj.save()
        return self.response_change(request, obj)

    def save_model(self, request, obj, form, change):
        """Overriding the save_model method to update jwt_token."""
        if change and 'jwt_token' in form.changed_data:
            exp_datetime = dt.datetime.utcnow() + dt.timedelta(
                days=JWT_TOKEN_EXTERNAL_SERVICES
            )
            payload = {
                "service_name": obj.service_name,
                "exp": exp_datetime,
                "iat": dt.datetime.utcnow(),
            }
            secret_key = SECRET_KEY_SERVICE
            obj.jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
        super().save_model(request, obj, form, change)


admin.site.register(Services, ServicesAdmin)

# from django import forms
# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django_scopes.forms import SafeModelChoiceField
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.forms import UserChangeForm
# from django.contrib.auth.models import Group

# from utils.admin import custom_titled_filter
# from accounts.models import Role
# from companies.models import Company


# User = get_user_model()
# admin.site.unregister(Group)


# class UserAdminForm(UserChangeForm):
#     """
#     Custom User admin form that exposes user roles.
#     """

#     role = forms.ModelChoiceField(queryset=Role.objects.none(), empty_label=None)

#     class Meta:
#         model = User
#         exclude = ()  # Required for Django
#         field_classes = {
#             "company": SafeModelChoiceField,
#         }

#     def __init__(self, *args, **kwargs):
#         super(UserAdminForm, self).__init__(*args, **kwargs)
#         if "company" in self.fields:
#             self.fields["company"].queryset = Company.objects.all().order_by("name")
#         self.fields["role"].queryset = Role.objects.all()
#         self.initial["role"] = self.instance.role if self.instance.role else 3

#     def save(self, *args, **kwargs):
#         kwargs["commit"] = True
#         return super(UserAdminForm, self).save(*args, **kwargs)

#     def save_m2m(self):
#         self.instance.groups.set(
#             [
#                 self.instance.role,
#             ]
#         )


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     change_form_template = "loginas/change_form.html"
#     form = UserAdminForm

#     list_display = [
#         "email",
#         "first_name",
#         "last_name",
#         "phone_number",
#         "company",
#         "role",
#         "is_active",
#     ]
#     list_filter = (
#         (
#             "company__name",
#             custom_titled_filter("company", admin.RelatedFieldListFilter),
#         ),
#         ("groups__name", custom_titled_filter("role", admin.RelatedFieldListFilter)),
#         (
#             "is_superuser",
#             custom_titled_filter("superuser status", admin.FieldListFilter),
#         ),
#         ("is_active", custom_titled_filter("is active status", admin.FieldListFilter)),
#     )
#     fieldsets = (
#         (
#             None,
#             {
#                 "fields": (
#                     "email",
#                     "first_name",
#                     "last_name",
#                     "phone_number",
#                     "password",
#                     "company",
#                     "is_active",
#                     "date_joined",
#                 )
#             },
#         ),
#         (
#             "Permissions",
#             {"fields": ("role",)},
#         ),
#         ("Django Admin Permissions", {"fields": ("staff", "is_superuser")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2"),
#             },
#         ),
#     )
#     search_fields = ["email"]
#     ordering = ["email"]
#     filter_horizontal = ()
#     readonly_fields = ("date_joined",)

#     def has_view_permission(self, request, obj=None):
#         if not super().has_view_permission(request, obj):
#             return False

#         return self._has_object_permissions(request, obj)

#     def has_change_permission(self, request, obj=None):
#         if not super().has_change_permission(request, obj):
#             return False

#         return self._has_object_permissions(request, obj)

#     def has_delete_permission(self, request, obj=None):
#         if not super().has_delete_permission(request, obj):
#             return False

#         return self._has_object_permissions(request, obj)

#     def _has_object_permissions(self, request, obj):
#         if obj is None:
#             return True

#         # Super Admin can edit everything
#         if request.user.is_superuser:
#             return True

#         # No one can edit super admins
#         if obj.is_superuser:
#             return False

#         # Users without company can be edited by anyone
#         # This is a special case for newly craeted users
#         if obj.company is None:
#             return True

#         # Others can manage only own company
#         return request.user.company == obj.company

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)

#         # Superusers have all privileges
#         if request.user.is_superuser:
#             return form

#         # Do not allow to edit Superusers
#         if obj is not None and obj.is_superuser:
#             for field in form.base_fields:
#                 form.base_fields[field].disabled = True
#             return form

#         # Non superusers can't grant admin, staff, or is_superuser
#         disabled_fields = {
#             "admin",
#             "staff",
#             "is_superuser",
#         }

#         # others can't change company
#         if not request.user.is_staff:
#             disabled_fields |= {
#                 "company",
#             }

#         for field in disabled_fields:
#             if field in form.base_fields:
#                 form.base_fields[field].disabled = True

#         return form


# class RoleAdminForm(forms.ModelForm):
#     """
#     This form adds an additional select field for users in the role.
#     """

#     users = forms.ModelMultipleChoiceField(
#         User.objects.none(),
#         widget=admin.widgets.FilteredSelectMultiple("users", False),
#         required=False,
#     )

#     class Meta:
#         model = Role
#         exclude = ()  # Required for Django
#         widgets = {
#             "permissions": admin.widgets.FilteredSelectMultiple("permissions", False),
#         }

#     def __init__(self, *args, **kwargs):
#         super(RoleAdminForm, self).__init__(*args, **kwargs)
#         self.fields["users"].queryset = User.objects.all().order_by("email")
#         if self.instance.pk:
#             initial_users = self.instance.user_set.values_list("pk", flat=True)
#             self.initial["users"] = initial_users

#     def save(self, *args, **kwargs):
#         kwargs["commit"] = True
#         return super(RoleAdminForm, self).save(*args, **kwargs)

#     def save_m2m(self):
#         self.instance.user_set.clear()
#         self.instance.user_set.add(*self.cleaned_data["users"])


# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     form = RoleAdminForm

#     list_display = ["name", "role_user_count"]
#     list_filter = ["name"]
#     fieldsets = ((None, {"fields": ("name", "users", "permissions")}),)
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("name", "users", "permissions"),
#             },
#         ),
#     )
#     search_fields = ["name"]
#     ordering = ["name"]
#     filter_horizontal = ()

#     def role_user_count(self, obj):
#         return obj.user_set.count()
