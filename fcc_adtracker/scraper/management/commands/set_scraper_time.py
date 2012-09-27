from scraper.models import Scrape_Time
from django.core.management.base import BaseCommand




class Command(BaseCommand):
    requires_model_validation = False
    
    def handle(self, *args, **options):
        now = Scrape_Time.objects.create()