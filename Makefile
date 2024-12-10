PROJECT_DIR ?= auth-service
ENV ?= $(PROJECT_DIR)/.env
VENV ?= $(shell (cd $(PROJECT_DIR) && pipenv --venv))

.env:
	test -f $(ENV) && echo $(ENV) exists || cp $(PROJECT_DIR)/tpl.dev-app.env $(ENV)

activate:
	cd $(PROJECT_DIR) && pipenv shell

install_pipenv:
	pip install pipenv

install_deps: install_pipenv
	cd $(PROJECT_DIR) && pipenv run pip install -U setuptools && pipenv install

lint:
	(cd $(PROJECT_DIR) && pipenv run lint)

isort:
	(cd $(PROJECT_DIR) && pipenv run isort)

format: isort lint
	echo "Done"

test:
	cd $(PROJECT_DIR) && pipenv run pytest --create-db
