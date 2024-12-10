from accounts.models import User
from accounts.utils import LDAPManager
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    help = "Synchronize users in LDAP and Postgres."

    def self_print(self, message, message_type):
        if message_type == "ERROR":
            self.stdout.write(self.style.ERROR(message))
        if message_type == "WARNING":
            self.stdout.write(self.style.WARNING(message))
        if message_type == "SUCCESS":
            self.stdout.write(self.style.SUCCESS(message))

    def handle(self, *args, **kwargs):

        try:
            users = User.objects.all()
        except ObjectDoesNotExist:
            self.self_print(
                "There are no users in the Postgres database.",
                "ERROR",
            )
            return None

        with LDAPManager() as ldap_manager:
            ldap_users = ldap_manager.get_users_list()
            if not ldap_users:
                self.self_print(
                    "There are no users in the LDAP database.",
                    "WARNING",
                )
                return None

            django_user_uids = {str(user.id) for user in users}
            ldap_user_uids = {user["uid"] for user in ldap_users}

            users_to_add = django_user_uids - ldap_user_uids
            users_to_delete = ldap_user_uids - django_user_uids
            add = 0
            delete = 0
            updata = 0

            if users_to_delete:
                for uid in tqdm(users_to_delete):
                    ldap_manager.delete_user_by_uid(uid)
                    self.self_print(
                        f"User with UID {uid} deleted from LDAP.",
                        "SUCCESS",
                    )
                    delete += 1

            if users_to_add:
                for uid in tqdm(users_to_add):
                    user = User.objects.get(id=uid)
                    uid = str(user.id)
                    user_data = ldap_manager.create_user_data(user)
                    ldap_manager.add_new_user(user_data)
                    self.self_print(
                        f"User {user.email} added to LDAP.",
                        "SUCCESS",
                    )
                    add += 1
                self.self_print(
                    f"Added {len(users_to_add)} users.",
                    "SUCCESS",
                )

            for uid in tqdm(django_user_uids):
                user = User.objects.get(id=uid)
                changes = ldap_manager.create_user_data(user)
                ldap_manager.change_user_by_uid(user.id, changes["attributes"])
                self.self_print(
                    f"User with UID {uid} update datas from LDAP.",
                    "SUCCESS",
                )
                updata += 1

            self.self_print(
                f"Synchronization completed.\n"
                f"Added {add} users.\n"
                f"Deleted {delete} users.\n"
                f"Updatad {updata} users.",
                "SUCCESS",
            )
