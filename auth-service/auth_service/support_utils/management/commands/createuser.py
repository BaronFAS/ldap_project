from django.core.management.base import BaseCommand
from accounts.models import User, Company, Role

class Command(BaseCommand):
    help = 'Create a new user'

    def handle(self, *args, **options):
        email = input("Enter user email: ")
        password = input("Enter user password: ")
        first_name = input("Enter user first name: ")
        last_name = input("Enter user last name: ")
        staff = input("Is the user staff? (yes/no): ").lower() == 'yes'
        admin = input("Is the user admin? (yes/no): ").lower() == 'yes'

        company_name = input("Enter company name: ")
        company, created = Company.objects.get_or_create(name=company_name)

        if not created:
            self.stdout.write(
                self.style.WARNING(f'Company with name "{company_name}" already exists.')
            )

        roles = []
        while True:
            role_name = input("Enter user role (or leave blank to finish adding roles): ")
            if not role_name:
                break
            role, created = Role.objects.get_or_create(name=role_name)
            roles.append(role)

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            staff=staff,
            admin=admin,
            company=company,
            roles=roles
        )
        for role in roles:
            user.role.add(role)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created user {user} with email: {email}, company: {company_name}, and roles: {", ".join([r.name for r in roles])}'
            )
        )
