import ldap
import ldap.modlist as modlist

from ldap_project.constants import (
    # USERS,
    # USER,
    LDAP_SERVER,
    LDAP_ADMIN_DN,
    LDAP_ADMIN_PASSWORD,
    SEARCH_BASE,
    SEARCH_ATTRIBUTES
)
from ldap_project.utils import (
    encode_attributes,
    process_search_results_user_by_uid,
    process_search_results_users_list,
)


def change_user_by_uid(uid, changes):
    """
    Изменяет атрибуты пользователя по его uid.
    :param uid: uid пользователя
    :param changes: словарь с изменениями, например:
    {
    'cn': 'New Common Name',
    'sn': 'New Surname',
    'userPassword': 'newpassword'
    }
    :return: True, если изменения успешно применены, иначе False
    """
    ldap_conn = ldap.initialize(LDAP_SERVER)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
    search_filter = f"(uid={uid})"
    results = ldap_conn.search_s(
        SEARCH_BASE, ldap.SCOPE_SUBTREE, search_filter
    )

    if results:
        dn, entry = results[0]
        mod_list = []

        for attr, new_value in changes.items():
            if attr in entry:
                if isinstance(new_value, str):
                    mod_list.append(
                        (ldap.MOD_REPLACE, attr, new_value.encode('utf-8'))
                    )
                else:
                    mod_list.append(new_value)
            else:
                if isinstance(new_value, str):
                    mod_list.append(
                        (ldap.MOD_ADD, attr, new_value.encode('utf-8'))
                    )
                else:
                    mod_list.append(new_value)

        try:
            ldap_conn.modify_s(dn, mod_list)
            ldap_conn.unbind_s()
            return True
        except ldap.LDAPError as e:
            print(f"Error modifying user: {e}")
            ldap_conn.unbind_s()
            return False
    else:
        print(f"User with uid {uid} not found.")
        ldap_conn.unbind_s()
        return False


def delete_user_by_uid(uid):
    ldap_conn = ldap.initialize(LDAP_SERVER)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
    search_filter = f"(uid={uid})"
    results = ldap_conn.search_s(
        SEARCH_BASE, ldap.SCOPE_SUBTREE, search_filter
    )
    if results:
        dn, entry = results[0]
        ldap_conn.delete_s(dn)
        return True
    return False


def add_new_user(user):
    ldap_conn = ldap.initialize(LDAP_SERVER)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
    encoded_attributes = encode_attributes(user["attributes"])
    ldap_conn.add_s(user["dn"], modlist.addModlist(encoded_attributes))
    ldap_conn.unbind_s()


def add_new_user_list(users):
    ldap_conn = ldap.initialize(LDAP_SERVER)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
    for user in users:
        encoded_attributes = encode_attributes(user["attributes"])
        ldap_conn.add_s(user["dn"], modlist.addModlist(encoded_attributes))
    ldap_conn.unbind_s()


def get_users_list():
    ldap_conn = ldap.initialize(LDAP_SERVER)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
    search_filter = "(objectClass=inetOrgPerson)"
    results = ldap_conn.search_s(
        SEARCH_BASE, ldap.SCOPE_SUBTREE, search_filter, SEARCH_ATTRIBUTES
    )
    ldap_conn.unbind_s()
    return process_search_results_users_list(results)


def get_user_by_uid(uid):
    ldap_conn = ldap.initialize(LDAP_SERVER)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
    search_filter = f"(uid={uid})"
    results = ldap_conn.search_s(
        SEARCH_BASE, ldap.SCOPE_SUBTREE, search_filter, SEARCH_ATTRIBUTES
    )
    ldap_conn.unbind_s()
    return process_search_results_user_by_uid(results)


if __name__ == "__main__":
    # add_new_user(USER)
    # add_new_user_list(USERS)
    users = get_users_list()
    for user in users:
        print(user)
    # uid = "testuser10"
    # if user := get_user_by_uid(uid):
    #     print(user)
    # else:
    #     print(f"User with uid {uid} not found")
    # if delete_user_by_uid(uid):
    #     print(f"User with uid {uid} has been deleted.")
    # else:
    #     print(f"User with uid {uid} not found.")
    # changes = {
    #     'cn': 'New Common Name',
    #     'sn': 'New Surname',
    #     'userPassword': 'newpassword'
    # }
    # if change_user_by_uid(uid, changes):
    #     print(f"User with uid {uid} has been updated.")
    # else:
    #     print(f"Failed to update user with uid {uid}.")
