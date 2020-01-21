from django.core.management.base import BaseCommand
from news.crawlers.bbc_crawler import run


class Command(BaseCommand):
    help = 'Run BBC News crawler'

    def handle(self, *args, **options):
        run()
