import factory
import jwt

from pathlib import Path
from datetime import datetime, timedelta

from django.contrib.auth.models import Permission

# import factory.fuzzy
from accounts.models import Role, User
from external_services.models import Services
from companies.models import Company
from auth_service.config import SECRET_KEY_SERVICE

test_dir_path = Path(__file__).parent


class ServicesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Services

    service_name = factory.Faker('word')
    jwt_token = factory.LazyAttribute(
        lambda obj: generate_jwt_token(obj.service_name)
    )
    service_url = factory.Faker('url')


def generate_jwt_token(service_name):
    """
    Helper function to generate a JWT token for the service.
    """
    payload = {
        'service_name': service_name,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY_SERVICE, algorithm='HS256')


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    short_name = factory.Faker("company_suffix")
    domain_url = factory.Faker("domain_name")
    password_reset_uri = factory.Faker("uri")


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = factory.Faker("name")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Faker("phone_number")
    is_active = True
    company = factory.SubFactory(CompanyFactory)

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for role in extracted:
                self.roles.add(role)


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission
