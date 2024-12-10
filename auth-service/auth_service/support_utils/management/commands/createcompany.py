from django.core.management.base import BaseCommand

from companies.models import Company


class Command(BaseCommand):
    help = 'Create a new company'

    def handle(self, *args, **options):
        name = input("Enter company name: ")
        short_name = input("Enter company short name: ")
        domain_url = input("Enter company domain URL: ")
        password_reset_uri = input("Enter company password reset URI: ")

        company = Company.objects.create(
            name=name,
            short_name=short_name,
            domain_url=domain_url,
            password_reset_uri=password_reset_uri
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'A {company.name} was created with id: {company.id}'
                )
            )
