import logging
import pytest
import ldap

from unittest.mock import patch, MagicMock
from typing import List, Dict, Union, Generator, Any

from accounts.models import User
from accounts.utils import LDAPManager
from auth_service.settings import SEARCH_BASE

logger = logging.getLogger(__name__)


@pytest.fixture
def user(user_factory):
    """A fixture that creates a user."""
    return user_factory()


@pytest.fixture
def mock_ldap() -> Generator[MagicMock, None, None]:
    """We simulate a connection to the LDAP."""
    with patch('ldap.initialize', return_value=MagicMock()) as mock_init:
        yield mock_init


class TestLDAPManager:

    @staticmethod
    def _generate_test_data(user: User) -> Dict[str, Union[str, None]]:
        """Generate test data for a user."""
        return {
            "cn": user.first_name,
            "sn": user.last_name,
            "mail": user.email,
            "uid": str(user.id),
            "telephoneNumber": user.phone_number
        }

    @staticmethod
    def _generate_mock_ldap_users(users: List[User]) -> List[tuple]:
        """Generate test data for a users in ldap."""
        users_list = []
        for user in users:
            users_list.append((
                f"uid={user.id},{SEARCH_BASE}", {
                    "cn": [user.first_name.encode('utf-8')],
                    "sn": [user.last_name.encode('utf-8')],
                    "mail": [user.email.encode('utf-8')],
                    "uid": [str(user.id).encode('utf-8')],
                    "telephoneNumber": [user.phone_number.encode('utf-8')]
                }
            ))
        return users_list

    @pytest.mark.django_db
    def test_change_user_by_uid(
        self, mock_ldap: MagicMock, user: User
    ) -> None:
        """
        Test the change_user_by_uid method of LDAPManager.
        """
        with LDAPManager() as ldap_manager:
            ml_rv = mock_ldap.return_value
            ml_rv.search_s.return_value = self._generate_mock_ldap_users(
                [user]
            )
            dn = f"uid={user.id},{SEARCH_BASE}"
            changes = {
                'cn': 'New_Name',
                'mail': 'new_email@example.com'
            }

            user_changed = ldap_manager.change_user_by_uid(user.id, changes)
            assert user_changed is True

            # Проверка, что modify_s был вызван с правильными аргументами
            expected_mod_list = [
                (ldap.MOD_REPLACE, 'cn', b'New_Name'),
                (ldap.MOD_REPLACE, 'mail', b'new_email@example.com')
            ]
            ml_rv.modify_s.assert_called_once_with(
                dn, expected_mod_list
            )

    @pytest.mark.django_db
    def test_delete_user_by_id(self, mock_ldap: MagicMock, user: User) -> None:
        """
        Test the delete_user_by_uid method of LDAPManager.
        """
        with LDAPManager() as ldap_manager:
            uid = str(user.id)
            dn = f"uid={uid},{SEARCH_BASE}"
            # Настройка мок для поиска пользователя
            mock_ldap.return_value.search_s.return_value = [(dn, {})]

            user_deleted = ldap_manager.delete_user_by_uid(uid)
            assert user_deleted is True
            # Проверка, что delete_s был вызван с правильным DN
            mock_ldap.return_value.delete_s.assert_called_once_with(dn)

            # Проверка, что search_s был вызван с правильными аргументами
            mock_ldap.return_value.search_s.assert_called_once_with(
                SEARCH_BASE, ldap.SCOPE_SUBTREE, f"(uid={uid})"
            )

    @pytest.mark.django_db
    def test_add_new_user(self, mock_ldap: MagicMock, user: User) -> None:
        """
        Test the add_user_by_uid method of LDAPManager.
        """
        with LDAPManager() as ldap_manager:
            ldap_conn = mock_ldap.return_value

            user_data = {
                "dn": f"uid={user.id},{SEARCH_BASE}",
                "attributes": self._generate_test_data(user)
            }
            ldap_manager.add_new_user(user_data)

            # Проверка, что метод add_s был вызван с правильными параметрами
            ldap_conn.add_s.assert_called_once()
            called_kwargs = ldap_conn.add_s.call_args[0]

            data = dict(called_kwargs[1])
            decoded_data = {
                key: value.decode('utf-8') for key, value in data.items()
            }
            assert decoded_data == user_data["attributes"]

    @pytest.mark.django_db
    def test_get_users_list(
        self, mock_ldap: MagicMock, user_factory: Any
    ) -> None:
        """
        Test the get_users_list method of LDAPManager.
        """
        with LDAPManager() as ldap_manager:
            users = user_factory.create_batch(3)
            ml_rv = mock_ldap.return_value
            ml_rv.search_s.return_value = self._generate_mock_ldap_users(users)
            expected_users = []
            for user in users:
                expected_users.append(self._generate_test_data(user))

            users_from_ldap = ldap_manager.get_users_list()
            assert users_from_ldap == expected_users

    @pytest.mark.django_db
    def test_get_user_by_uid(self, mock_ldap: MagicMock, user: User) -> None:
        """
        Test the get_user_by_uid method of LDAPManager.
        """
        with LDAPManager() as ldap_manager:
            ml = mock_ldap.return_value.search_s
            ml.return_value = self._generate_mock_ldap_users([user])
            user_from_ldap = ldap_manager.get_user_by_uid(user.id)
            assert user_from_ldap == self._generate_test_data(user)
