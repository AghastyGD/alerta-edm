from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

from django.conf import settings
from datetime import datetime
from .models import PowerOutage

class PowerOutageScraper:
    def __init__(self, browser=settings.BROWSER):
        self.browser = browser.lower()
        self.driver = self.get_driver()

    def get_driver(self):
        if self.browser == "chrome":
            chrome_path = ChromeDriverManager().install()
            
            if 'THIRD_PARTY_NOTICES.chromedriver' in chrome_path:
                chrome_path = chrome_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver')
                
            chrome_options = self.get_chrome_options()
            service = ChromeService(executable_path=chrome_path)
            return webdriver.Chrome(service=service, options=chrome_options)
        elif self.browser == "firefox":
            firefox_options = self.get_firefox_options()
            service = FirefoxService(executable_path=GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=firefox_options)
        else:
            raise ValueError(f"Browser '{self.browser}' is not supported!")

    def get_chrome_options(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return chrome_options

    def get_firefox_options(self):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        return firefox_options

    def scrape(self):
        url = "https://www.edm.co.mz/manutencao" 
        self.driver.get(url)
        
        event_items = self.driver.find_elements(By.CLASS_NAME, "event2_item")
        for event in event_items:
            try:
                area, state, affected_zone, date, time_periods = self.extract_event_data(event)
                            
                # Save to the database
                self.save_power_outages(area, state, affected_zone, date, time_periods)

            except Exception:
                continue


    def extract_event_data(self, event):
        date_wrapper = event.find_element(By.CLASS_NAME, "event2_date-wrapper")
        day = date_wrapper.find_elements(By.TAG_NAME, "div")[1].text.strip()
        month_year = date_wrapper.find_elements(By.TAG_NAME, "div")[2].text.strip()
        start_time = date_wrapper.find_elements(By.TAG_NAME, "div")[3].text.strip()
        end_time = date_wrapper.find_elements(By.TAG_NAME, "div")[4].text.strip()

        # Parse date and multiple time periods
        date, time_periods = self.parse_date_time(day, month_year, start_time, end_time)

        # Extract area, state and affected zone
        area = event.find_element(By.CLASS_NAME, "event2_tag-item").text.strip()  
        state = event.find_elements(By.CLASS_NAME, "heading-style-h5")[1].text.strip()
        affected_zone = event.find_element(By.CLASS_NAME, "text-size-regular").text.strip()
        
        if "Cidade de" in state:
            state = state 
        else:
            if not state.startswith("Província de"):
                state = f"Província de {state}"

        return area, state, affected_zone, date, time_periods

    def parse_date_time(self, day, month_year, start_time, end_time):
        # convert to datetime
        full_date_str = f"{day} {month_year}"
        date = datetime.strptime(full_date_str, "%d %B %Y").date()

        # format time periods
        time_periods = [(datetime.strptime(start_time, "%H:%M").time(),
                        datetime.strptime(end_time, "%H:%M").time())]
        
        return date, time_periods

    def save_power_outages(self, area, state, affected_zone, date, time_periods):
        for start_time, end_time in time_periods:
            # Check for existing records to avoid duplicates
            if not PowerOutage.objects.filter(
                area=area,
                state=state,
                affected_zone=affected_zone,
                date=date,
                start_time=start_time,
                end_time=end_time
            ).exists():
                PowerOutage.objects.create(
                    area=area,
                    state=state,
                    affected_zone=affected_zone,
                    date=date,
                    start_time=start_time,
                    end_time=end_time
                )
