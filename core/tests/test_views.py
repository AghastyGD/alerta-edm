from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from core.scraper import PowerOutageScraper
from core.models import PowerOutage
from datetime import date, time
from django.utils import timezone


class RunScrapingViewTest(TestCase):
    
    @patch.object(PowerOutageScraper, 'scrape')
    def test_run_scraping_success(self, mock_scrape):
        """Tests if scraping is successful"""
        mock_scrape.return_value = None  
        
        response = self.client.get(reverse('run_scraper')) 
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'success', 'message': 'Scraping completed successfully!'}
        )

    @patch.object(PowerOutageScraper, 'scrape') 
    def test_run_scraping_error(self, mock_scrape):
        """Test if the error is handled correctly during scraping"""
        mock_scrape.side_effect = Exception("Erro no scraping")
        
        response = self.client.get(reverse('run_scraper'))  
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'error', 'message': 'Erro no scraping'}
        )

class PowerOutageListViewTest(TestCase):

    def setUp(self):
        today = timezone.now().date()
        PowerOutage.objects.create(
            area='Area 1',
            state='State 1',
            affected_zone='Zone 1',
            date=today + timezone.timedelta(days=1),
            start_time=time(8, 0),
            end_time=time(12, 0)
        )
        PowerOutage.objects.create(
            area='Area 2',
            state='State 2',
            affected_zone='Zone 2',
            date=today - timezone.timedelta(days=1),
            start_time=time(8, 0),
            end_time=time(12, 0)
        )
    
    def test_power_outage_list(self):
        """Tests if the future and past outages are listed correctly in the list view."""
        response = self.client.get(reverse('power_outage_list')) 
        self.assertEqual(response.status_code, 200)
        
        self.assertIn('future_outages', response.context)
        self.assertGreater(len(response.context['future_outages']), 0)  
        
        self.assertIn('past_outages', response.context)
        self.assertGreater(len(response.context['past_outages']), 0) 

    def test_grouping_of_future_outages(self):
        """Test if future outages are grouped correctly by date"""
        today = timezone.now().date()
        PowerOutage.objects.create(
            area='Area 3',
            state='State 3',
            affected_zone='Zone 3',
            date=today + timezone.timedelta(days=1),
            start_time=time(9, 0),
            end_time=time(11, 0)
        )
        response = self.client.get(reverse('power_outage_list')) 
        future_outages = response.context['future_outages']
        self.assertEqual(len(future_outages), 1)  
        self.assertEqual(len(future_outages[0]['outages']), 2) 
        
class PowerOutageDetailViewTest(TestCase):

    def setUp(self):
        today = timezone.now().date()
        self.power_outage = PowerOutage.objects.create(
            area='Area 1',
            state='State 1',
            affected_zone='Zone 1',
            date=today + timezone.timedelta(days=1),
            start_time=time(8, 0),
            end_time=time(12, 0),
        )

    def test_power_outage_detail_view(self):
        """Tests if the detail view displays the correct power outage info. """
        response = self.client.get(reverse('power_outage_detail', kwargs={'slug': self.power_outage.slug}))  
        self.assertEqual(response.context['outage'], self.power_outage)  # 

    def test_power_outage_detail_not_found(self):
        """Test if the detail view returns a 404 error if the power outage is not found"""
        response = self.client.get(reverse('power_outage_detail', kwargs={'slug': 'invalid-slug'})) 
        self.assertEqual(response.status_code, 404)