from pprint import pformat

from accounts.models import User
from accounts.utils import LDAPManager
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get user list in LDAP"

    def handle(self, *args, **kwargs):

        if not User.objects.exists():
            self.stdout.write(
                self.style.ERROR("There are no users in the database.")
            )
            return
        with LDAPManager() as ldap_manager:
            ldap_users = ldap_manager.get_users_list()
            formatted_users = pformat(ldap_users)
            self.stdout.write(self.style.SUCCESS("Your user:"))
            self.stdout.write(formatted_users)
