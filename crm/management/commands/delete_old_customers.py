from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "delete old customer data"

    def handle(self, *args, **kwargs):
        inactive_customers = Customer.objects.exclude(
            orders__created_at__gte=one_year_ago
        ).distinct()

        count = inactive_customers.count()
        inactive_customers.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {count} inactive customer(s)."
        ))