# LDAP

## What to do when you first start?

go to dir
```bash
cd ldap-infra
```

start docker
```bash
sudo docker compose up --build
```

go to in docker container
```bash
sudo docker exec -it openldap /bin/bash
```

create files users.ldif and create_ou.ldif
```bash
apt-get update
apt-get install nano
nano users.ldif
```

exampe file user.ldif
```bash
dn: uid=<uid>,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
cn: <first_name>
sn: <last_name>
mail: <user_email>
uid: <uid>
userPassword: <hashed_password>
telephoneNumber: <phone_number>
```
exampe file create_ou.ldif
```bash
dn: ou=users,dc=example,dc=com
objectClass: organizationalUnit
ou: users
description: Organizational Unit for Users
```

TODO спросить Ваню.
or one file user.ldif
```bash
dn: ou=users,dc=example,dc=com
objectClass: organizationalUnit
ou: users
description: Organizational Unit for Users

dn: uid=<uid>,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
cn: <first_name>
sn: <last_name>
mail: <user_email>
uid: <uid>
userPassword: <hashed_password>
telephoneNumber: <phone_number>
```

Use the ldapadd command to add this OU to your LDAP server:
```bash
ldapadd -x -D "cn=admin,dc=example,dc=com" -w your-admin-password -f create_ou.ldif
```

exit the docker container, go to dir with file manage.py
and perform a test user creation with the command:
(the user must be created in django db)
```bash
python manage.py add_new_user_in_ladp email@email.you_user
```
