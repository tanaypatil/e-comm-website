from django.core.management.base import BaseCommand
from managing_users.models import NFLMUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not NFLMUser.objects.filter(username="mansoormohd").exists():
            NFLMUser.objects.create_superuser(username="mansoormohd", email="skmansoormohd@gmail.com", mobile="7387493229", password="Scz@7209")
