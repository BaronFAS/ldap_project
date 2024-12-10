import logging
from typing import Dict, List, Optional, Union

import ldap
import ldap.modlist as modlist
from auth_service.settings import (LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD,
                                   LDAP_SERVER, SEARCH_ATTRIBUTES, SEARCH_BASE)

logger = logging.getLogger(__name__)


class LDAPManager:
    ldap_server = LDAP_SERVER
    admin_dn = LDAP_ADMIN_DN
    admin_password = LDAP_ADMIN_PASSWORD
    search_base = SEARCH_BASE
    search_attributes = SEARCH_ATTRIBUTES

    def __init__(self):
        self.ldap_conn = None

    def __enter__(self) -> "LDAPManager":
        self.ldap_conn = ldap.initialize(self.ldap_server)
        self.ldap_conn.simple_bind_s(self.admin_dn, self.admin_password)
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        traceback: Optional[Exception],
    ) -> Optional[bool]:
        if self.ldap_conn:
            self.ldap_conn.unbind_s()
        if exc_type is not None:
            logging.error(f"Exception type: {exc_type}")
            logging.error(f"Exception value: {exc_value}")
            logging.error(f"Traceback: {traceback}")
        return False

    def _process_entry(
        self, entry: Dict[str, Union[str, List[bytes]]]
    ) -> Dict[str, str]:
        """
        Process an LDAP entry to decode byte values to string.
        """
        processed_entry = {}
        for attr, values in entry.items():
            if isinstance(values[0], bytes):
                processed_entry[attr] = values[0].decode("utf-8")
            else:
                processed_entry[attr] = values[0]
        return processed_entry

    def _process_search_results_user_by_uid(
        self, results: List[tuple]
    ) -> Optional[Dict[str, str]]:
        """
        Process search results to find a user by UID.
        """
        if results:
            dn, entry = results[0]
            return self._process_entry(entry)
        return None

    def _process_search_results_users_list(
        self, results: List[tuple]
    ) -> List[Dict[str, str]]:
        """
        Process search results to get a list of users.
        """
        users = []
        for dn, entry in results:
            if dn:
                users.append(self._process_entry(entry))
        return users

    def _encode_attributes(
        self, attributes: Dict[str, Union[str, List[str]]]
    ) -> Dict[str, List[bytes]]:
        """
        Encode attributes to be suitable for LDAP operations.
        """
        encoded_attributes = {}
        for key, value in attributes.items():
            if isinstance(value, list):
                encoded_attributes[key] = [
                    str(v).encode("utf-8") for v in value
                ]
            else:
                encoded_attributes[key] = str(value).encode("utf-8")
        return encoded_attributes

    def _prepare_mod_list(
        self,
        entry: Dict[str, Union[str, List[bytes]]],
        changes: Dict[str, Union[str, List[str]]],
    ) -> List[tuple]:
        """
        Prepare a modification list for LDAP operations.
        """
        mod_list = []
        for attr, new_value in changes.items():
            if isinstance(new_value, str):
                new_value = new_value.encode("utf-8")
            if attr not in entry:
                mod_list.append((ldap.MOD_ADD, attr, new_value))
            mod_list.append((ldap.MOD_REPLACE, attr, new_value))
        return mod_list

    def create_user_data(
        self,
        user: object,
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        """
        Create user data dictionary for LDAP operations.
        """
        user_data = {
            "dn": f"uid={user.id},ou=users,dc=example,dc=com",
            "attributes": {
                "objectClass": ("inetOrgPerson"),
                "cn": user.first_name or "None",
                "sn": user.last_name or "None",
                "mail": user.email,
                "uid": user.id,
                "userPassword": user.secret_key or "None",
                "telephoneNumber": user.phone_number or "None",
            },
        }
        return user_data

    def change_user_by_uid(
        self,
        uid: str,
        changes: Dict[str, Union[str, List[str]]],
    ) -> bool:
        """
        Change user attributes by UID.
        """
        logging.info(f"UID: {uid}")
        logging.info(f"CHANGES: {changes}")
        search_filter = f"(uid={uid})"
        results = self.ldap_conn.search_s(
            self.search_base, ldap.SCOPE_SUBTREE, search_filter
        )
        logging.info(f"RESULT {results}")
        if not results:
            logging.info(f"User with uid {uid} not found in LDAP.")
            return False
        dn, entry = results[0]
        mod_list = self._prepare_mod_list(entry, changes)
        if not mod_list:
            logging.info(f"No changes to apply for user with uid {uid}.")
            return True
        try:
            self.ldap_conn.modify_s(dn, mod_list)
            return True
        except ldap.LDAPError as e:
            logging.error(f"Error LDAP modifying user: {e}")
            return False

    def delete_user_by_uid(self, uid: str) -> bool:
        """
        Delete a user by UID.
        """
        search_filter = f"(uid={uid})"
        results = self.ldap_conn.search_s(
            self.search_base, ldap.SCOPE_SUBTREE, search_filter
        )
        if not results:
            return False
        dn, entry = results[0]
        self.ldap_conn.delete_s(dn)
        return True

    def add_new_user(
        self,
        user: Dict[str, Union[str, Dict[str, str]]],
    ) -> None:
        """
        Add a new user to LDAP.
        """
        encoded_attributes = self._encode_attributes(user["attributes"])
        self.ldap_conn.add_s(
            user["dn"],
            modlist.addModlist(encoded_attributes)
        )

    def get_users_list(self) -> List[Dict[str, str]]:
        """
        Get a list of all users from LDAP.
        """
        search_filter = "(objectClass=inetOrgPerson)"
        results = self.ldap_conn.search_s(
            self.search_base,
            ldap.SCOPE_SUBTREE,
            search_filter,
            self.search_attributes,
        )
        return self._process_search_results_users_list(results)

    def get_user_by_uid(self, uid: str) -> Optional[Dict[str, str]]:
        """
        Get a user by UID.
        """
        search_filter = f"(uid={uid})"
        results = self.ldap_conn.search_s(
            self.search_base,
            ldap.SCOPE_SUBTREE,
            search_filter,
            self.search_attributes,
        )
        return self._process_search_results_user_by_uid(results)
