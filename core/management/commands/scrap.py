from core.scraper import PowerOutageScraper
from django.core.management.base import BaseCommand
import traceback

class Command(BaseCommand):
    help = 'Scrape and save power outage information'

    def handle(self, *args, **options):
        try: 
            scraper = PowerOutageScraper()
            scraper.scrape()  
            return self.stdout.write(self.style.SUCCESS('Scraping completed successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Scraping failed: {str(e)}"))
            traceback.print_exc()
