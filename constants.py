# Определение тестовых пользователей
USERS = [
    {
        "dn": "uid=testuser9,ou=users,dc=example,dc=com",
        "attributes": {
            "objectClass": ["inetOrgPerson"],
            "cn": "Test User9",
            "sn": "User9",
            "uid": "testuser9",
            "userPassword": "testpassword"
        }
    },
    {
        "dn": "uid=testuser10,ou=users,dc=example,dc=com",
        "attributes": {
            "objectClass": ["inetOrgPerson"],
            "cn": "Test User10",
            "sn": "User10",
            "uid": "testuser10",
            "userPassword": "testpassword"
        }
    }
]
USER = {
    "dn": "uid=testuser11,ou=users,dc=example,dc=com",
    "attributes": {
        "objectClass": ["inetOrgPerson"],
        "cn": "Test User11",
        "sn": "User11",
        "uid": "testuser11",
        "userPassword": "testpassword"
        }
}

# Параметры подключения к LDAP серверу
LDAP_SERVER = "ldap://localhost"
LDAP_ADMIN_DN = "cn=admin,dc=example,dc=com"
LDAP_ADMIN_PASSWORD = "admin"
SEARCH_BASE = "ou=users,dc=example,dc=com"
SEARCH_ATTRIBUTES = ["uid", "cn", "sn"]
