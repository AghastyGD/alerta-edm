from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

import re
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
        url = "https://www.edm.co.mz/pt/website-intranet-mobile/page/cortes-programados"
        self.driver.get(url)

        rows = self.driver.find_elements(By.XPATH, "//table//tr")
        for row in rows:
            cells = row.find_elements(By.XPATH, ".//td | .//th")

            if not cells or "ÁREA" in cells[0].text:
                continue

            try:
                # Extract and parse data
                area, province, zones, date_time_text = self.extract_row_data(cells)
                date, time_periods = self.parse_date_and_multiple_times(date_time_text)

                # Save to the database
                self.save_power_outages(area, province, zones, date, time_periods)

            except IndexError:
                continue

        self.driver.quit()

    def extract_row_data(self, cells):
        area = cells[0].text.strip() if len(cells) > 0 else 'N/A'
        province = cells[1].text.strip() if len(cells) > 1 else 'N/A'
        zones = cells[2].text.strip() if len(cells) > 2 else 'N/A'
        date_time_text = ' '.join([p.text.strip() for p in cells[3].find_elements(By.TAG_NAME, 'p')]) if len(cells) > 3 else 'N/A'
        return area, province, zones, date_time_text

    def parse_date_and_multiple_times(self, date_and_time_text):
        date_match = re.search(r'\d{2}/\d{2}/\d{4}', date_and_time_text)
        time_matches = re.findall(r'(\d{2}:\d{2}) às (\d{2}:\d{2})', date_and_time_text)

        if date_match and time_matches:
            date_str = date_match.group(0)
            date = datetime.strptime(date_str, "%d/%m/%Y").date()

            time_periods = [
                (datetime.strptime(start_time, "%H:%M").time(),
                 datetime.strptime(end_time, "%H:%M").time())
                for start_time, end_time in time_matches
            ]

            return date, time_periods

        return None, []

    def save_power_outages(self, area, province, zones, date, time_periods):
        for start_time, end_time in time_periods:
            # Check for existing records to avoid duplicates
            if not PowerOutage.objects.filter(
                area=area,
                state=province,
                affected_zone=zones,
                date=date,
                start_time=start_time,
                end_time=end_time
            ).exists():
                PowerOutage.objects.create(
                    area=area,
                    state=province,
                    affected_zone=zones,
                    date=date,
                    start_time=start_time,
                    end_time=end_time
                )
