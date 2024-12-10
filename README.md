# Auth Service

auth-service is a service containing information about users, resources and their access and API to manage them.

# Development

## Option: Pipenv

### Install requirements

```bash
# configure sources
# we use custom PyPi for packages

# install ALL deps from Pipfile.lock
make install_deps

# final message
echo "Ready for development"
```

### Install dev requirements

```bash
# configure sources
# we use custom PyPi for packages

# install ALL deps from Pipfile.lock
make install_deps 
# final message
echo "Ready for development"
````
#### or use this:
```bash
# change dir
cd auth-service
# run install deps
pipenv install -d
```

### Run tests:
```bash
# change dir
cd auth-service
# start tests
pipenv run pytest --create-db
```
To successfully complete the LDAP tests, you need to launch a docker container with it. To do this, go to the ldap-infra folder and run the command:
```
docker compose up --build
```

# Deployment

- Make Pull request
- Take app in preview environment
- Approve it from colleagues
- Take app in staging environment

# Codestyle

To control the codestyle and use [flakeheaven](https://flakeheaven.readthedocs.io/en/latest/), 
the old code will be brought to the actual codestyle gradually,
the new code must match the current codestyle settings

`flake8`/`flakeheaven` configuration and its extensions stored in `pyproject.toml`

**Autoformat code**

```shell
# run from repo root
make format 

# or 
pipenv run black && pipenv run isort && pipenv run lint
```

**Run for new code:**

```shell
pipenv run lint
```

**Run for new + old code:**

```shell
pipenv run flint
```

**Automatically optimize imports ordering and format:**

```shell
pipenv run isort
```

# Additional commands for manual testing

**Before running the commands:**

```shell
# Go to the auth_service folder
cd auth_service
# Start the virtual environment
pipenv shell
# Go to the auth_service folder where the manage.py file is located
cd auth_service
```
**Now you can create a simple User, Role and Company for testing:**

```shell
python manage.py createuser
```

```shell
python manage.py createrole
```

```shell
python manage.py createcompany
```

# Additional commands for LDAP

```shell
python manage.py add_user_in_ldap.py
```

```shell
python manage.py del_user_in_ldap.py
```

```shell
python manage.py get_user_in_ldap.py
```

```shell
python manage.py get_users_list_in_ldap.py
```

```shell
# Synchronize users in LDAP and Postgres.
# Priority for Postgres.
python manage.py ldap_synchronize.py
```
