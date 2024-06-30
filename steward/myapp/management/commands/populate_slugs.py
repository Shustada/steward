from django.core.management.base import BaseCommand
from myapp.models import WorkAddress
from autoslug.utils import generate_unique_slug

class Command(BaseCommand):
    help = 'Populate slug field for existing WorkAddress records'

    def handle(self, *args, **kwargs):
        for work_address in WorkAddress.objects.all():
            if not work_address.slug:
                work_address.slug = generate_unique_slug(WorkAddress, 'slug', work_address.address)
                work_address.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated slug for: {work_address.address}'))
