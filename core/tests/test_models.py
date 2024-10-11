from django.test import TestCase
from datetime import date, time
from core.models import PowerOutage

class PowerOutageModelTest(TestCase):
    
    def setUp(self):
        self.power_outage = PowerOutage.objects.create(
            area='ASC CHIMOIO',
            state='Manica',
            affected_zone='Distritos de Macate e Sussundenga.',
            date=date(2023, 12, 2),
            start_time=time(6, 0),
            end_time=time(15, 0),
        )

    def test_power_outage_creation(self):
        """Test if the object was created correctly."""
    
        self.assertEqual(PowerOutage.objects.count(), 1)

        self.assertEqual(self.power_outage.area, 'ASC CHIMOIO')
        self.assertEqual(self.power_outage.state, 'Manica')
        self.assertEqual(self.power_outage.affected_zone, 'Distritos de Macate e Sussundenga.')
        self.assertEqual(self.power_outage.date, date(2023, 12, 2))
        self.assertEqual(self.power_outage.start_time, time(6, 0))
        self.assertEqual(self.power_outage.end_time, time(15, 0))
    
    def test_slug_auto_generation(self):
        """Test if the slug was generated correctly."""
        self.assertEqual(self.power_outage.slug, 'manica')
    
    def test_power_outage_str_method(self):
        """Test if the __str__ method was correctly implemented."""
        self.assertEqual(str(self.power_outage), "ASC CHIMOIO - Manica")
    
    def test_date_field_type(self):
        """Test if the date field was correctly set to date."""
        self.assertIsInstance(self.power_outage.date, date)
    
   
