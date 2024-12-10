from accounts.models import User
from accounts.utils import LDAPManager
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete user in LDAP"

    def add_arguments(self, parser):
        parser.add_argument(
            "user_email",
            type=str,
            help="Email of an existing user in the database",
        )

    def handle(self, *args, **kwargs):

        user_email = kwargs["user_email"]
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f"User with email {user_email} does not exist."
                )
            )
            return

        with LDAPManager() as ldap_manager:
            ldap_manager.delete_user_by_uid(user.id)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully delete user {user_email}")
            )
