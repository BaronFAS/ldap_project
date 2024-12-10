from accounts.models import User
from accounts.utils import LDAPManager
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Add a new user to LDAP"

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
            return None

        with LDAPManager() as ldap_manager:
            user_data = ldap_manager.create_user_data(user)
            ldap_manager.add_new_user(user_data)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added user {user_data}")
            )
