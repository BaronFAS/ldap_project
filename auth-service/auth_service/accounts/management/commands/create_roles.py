from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from accounts.models import Role


# Viewer has only access to FMS and analytics for the specific site,
# and only can view it. Can not do any modifications (add new stop,
# do the remote control, plan a mission, update semantic map, etc.).
viewer_role_codenames = [
    "view_user",
    "view_company",
    "view_site",
    "view_fleet",
    "view_localizationmap",
    "view_semanticmap",
    "view_mission",
    "view_missionqueue",
    "view_stop",
    "view_vehicleconfiguration",
    "view_vehicletype",
    "view_vehicle",
    # User management
    "change_their_avatar",
    "view_queuedmission",
    "view_deployment",
    "view_vehicledeployment",
]

# Vehicle Operator has Viewer permissions plus can login to the vehicle
# dashboard (for the site it belongs too).
vehicle_operator_codenames = viewer_role_codenames + [
    # TODO Add permissions for vehicle operator
]

# Mission Operator has Vehicle Operator permissions plus can do
# mission planning (for the site it belongs too).
mission_operator_codenames = vehicle_operator_codenames + [
    # Mission management
    "add_mission",
    "change_mission",
    "delete_mission",
    "add_missionqueue",
    "change_missionqueue",
    "delete_missionqueue",
    "add_queuedmission",
    "change_queuedmission",
    # Deployment management
    "add_deployment",
    "change_deployment",
    "add_vehicledeployment",
    "change_vehicledeployment",
]

# Remote Control Operator has Mission operator permissions plus can do
# remote control (for the site it belongs too).
remote_control_operator_codenames = mission_operator_codenames + []

# User has Remote Control Operator permissions plus can edit everything
# inside the site it belongs to except users manipulation (modify stops,
# missions, maps, etc.).
user_codenames = remote_control_operator_codenames + [
    # Fleet management
    "add_fleet",
    "change_fleet",
    "delete_fleet",
    # Maps management
    "add_localizationmap",
    "change_localizationmap",
    "delete_localizationmap",
    "add_semanticmap",
    "change_semanticmap",
    "delete_semanticmap",
    # Mission management
    "add_mission",
    "change_mission",
    "delete_mission",
    # Stop management
    "add_stop",
    "change_stop",
    "delete_stop",
    # Vehicle Configuration management
    "add_vehicleconfiguration",
    "change_vehicleconfiguration",
    "delete_vehicleconfiguration",
    # Vehicle Type management
    "add_vehicletype",
    "change_vehicletype",
    "delete_vehicletype",
    # Vehicle management
    "add_vehicle",
    "change_vehicle",
    "delete_vehicle",
]

# Editor has User permissions plus access to the cloud internal tools
# (configuration manager, map editor, TKOs, data collection, etc.).
# Also can edit analytics.
editor_codenames = user_codenames + [
    # TODO Add permission for editor
]

# Admin has User permissions plus can manipulate users and sites inside the
# company it belongs to (add new user, change user role, add new site, etc).
admin_codenames = user_codenames + [
    # Site management
    "add_site",
    "change_site",
    "delete_site",
    # Role and Permission management
    "view_role",
    "add_role",
    "change_role",
    "delete_role",
    "add_permission",
    "change_permission",
    "delete_permission",
    # User management
    "add_user",
    "change_user",
    "delete_user",
    "view_user_is_active",
    "change_user_data",
    "view_user_id",
]

# Super Admin has Editor and Admin permissions for all companies plus can
# manipulate companies (add, remove, modify).
# fmt: off
super_admin_codenames = editor_codenames + admin_codenames + [
    "add_company",
    "change_company",
    "delete_company",
    "view_remote_control",
    "can_remote_control",
    "view_user_id",
    "change_user_data",
]
# fmt: on


class Command(BaseCommand):
    """The command creates list of predefined user roles."""

    help = "Create predefined user roles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force-update",
            action="store_true",
            dest="force-update",
            default=False,
            help="Update permissions if role already exists",
        )

    def handle(self, *args, **options):
        """Handle the command"""
        force_update = options.get("force-update", False)
        self.create_role("Viewer", viewer_role_codenames, force_update)
        self.create_role("Vehicle Operator", vehicle_operator_codenames, force_update)
        self.create_role("Mission Operator", mission_operator_codenames, force_update)
        self.create_role("Remote Control Operator", remote_control_operator_codenames, force_update)
        self.create_role("User", user_codenames, force_update)
        self.create_role("Editor", editor_codenames, force_update)
        self.create_role("Admin", admin_codenames, force_update)
        self.create_role("Super Admin", super_admin_codenames, force_update)

        self.stdout.write(self.style.SUCCESS("Successfully created roles"))

    def create_role(self, name: str, codenames: list[str], force_update: bool) -> Role:
        """
        Create Role object with the given name and permissions
        specified by their codenames.
        """
        role, created = Role.objects.get_or_create(name=name)
        if created or force_update:
            codenames = set(codenames)
            permissions = Permission.objects.filter(codename__in=codenames).values_list("id", flat=True)
            role.permissions.set(permissions)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"'{name}' role has been created, permissions: {len(permissions)}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"'{name}' role has been updated, permissions: {len(permissions)}")
                )

        return role
