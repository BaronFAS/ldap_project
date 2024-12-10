from django.core.management.base import BaseCommand
from accounts.models import Role


class Command(BaseCommand):
    help = 'Create a new role'

    def add_arguments(self, parser):
        """The 'role_name' argument is optional;
        if it is not present in the 'python manage.py createrole RoleName'
        command, the role will be created with the default value."""
        parser.add_argument(
            'role_name',
            nargs='?',
            type=str,
            default='Default Role',
            help='Role name'
        )

    def handle(self, *args, **options):
        role_name = options['role_name']
        role = Role.objects.create(name=role_name)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {role} with name: {role_name}'
            )
        )
