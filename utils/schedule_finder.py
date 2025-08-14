import os
import time
from urllib3.exceptions import ProtocolError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (InvalidSessionIdException, TimeoutException,
                                        StaleElementReferenceException, NoSuchElementException)
from .interfaces import ScheduleFinderInterface


class ScheduleFinder(ScheduleFinderInterface):
    def get_scheduled_associates(self, display):
        """Main function to get scheduled AA logins for a given shift and date."""
        if not display.driver:
            need_attribute = True
            driver = self.setup_webdriver()

            try:
                self.login_to_site(driver, display)

            except (TypeError, ProtocolError, InvalidSessionIdException, TimeoutException,
                    StaleElementReferenceException, NoSuchElementException):
                display.driver.quit()
                return None, None
        else:
            need_attribute = False

        try:
            self.select_date(display.driver, display.date)
            self.select_shift(display.driver,
                              display.date.strftime("%a"),
                              display.date.strftime("%b"),
                              display.date.strftime("%d"),
                              display.shift)

            if need_attribute:
                self.open_attribute_panel(display.driver)

            logins = self.extract_logins(display.driver)

            return display.driver, logins

        except (TypeError, ProtocolError, InvalidSessionIdException, TimeoutException,
                StaleElementReferenceException, NoSuchElementException):
            display.driver.quit()
            return None, None

    def setup_webdriver(self):
        """Sets up the Selenium WebDriver with required options."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--headless")  # Remove for debugging
        return webdriver.Chrome(options=chrome_options)

    def login_to_site(self, driver, display):
        """Logs in to the website using OS login and the provided credentials."""
        wait = WebDriverWait(driver, timeout=10)
        driver.get(os.getenv('MIDWAY'))

        login = os.getlogin()
        wait.until(ec.visibility_of_element_located((By.ID, "user_name")))
        driver.find_element(By.ID, "user_name").send_keys(login)

        pin = display.midway_pin()
        driver.find_element(By.ID, "password").send_keys(pin)

        otp = display.security_key()
        driver.find_element(By.ID, "otp").send_keys(otp)
        driver.find_element(By.ID, "verify_btn").click()

        wait.until(lambda d: f"Welcome {login}" in d.find_element(By.TAG_NAME, "h1").text)

    def select_date(self, driver, date):
        """Selects the date in the date picker."""
        wait = WebDriverWait(driver, timeout=10)
        driver.get(os.getenv('SITE_URL'))
        wait.until(ec.visibility_of_element_located((By.ID, "date-picker")))

        month_num = date.month
        day = date.day
        year = date.strftime("%Y")

        # Enter the date twice to avoid issues
        for _ in range(2):
            date_entry = driver.find_element(By.ID, "date-picker")
            date_entry.send_keys(month_num)
            if month_num == 1:
                date_entry.send_keys(Keys.TAB)
            date_entry.send_keys(day)
            if day <= 3:
                date_entry.send_keys(Keys.TAB)
            date_entry.send_keys(year)

            driver.find_element(By.ID, "schedule-timeline-current-week-text").click()

    def select_shift(self, driver, day_of_week, month, day_decimal, shift):
        """Clicks the shift button for the given date and shift."""
        wait = WebDriverWait(driver, timeout=10)
        wait.until(ec.visibility_of_element_located((By.ID, f"time-cell-{day_of_week}-{month}-{day_decimal}-{shift}")))
        driver.find_element(By.ID, f"time-cell-{day_of_week}-{month}-{day_decimal}-{shift}").click()

    def open_attribute_panel(self, driver):
        """Opens the attribute panel and unchecks the unnecessary checkboxes."""
        wait_long = WebDriverWait(driver, timeout=60)
        wait_long.until(ec.visibility_of_element_located((By.CLASS_NAME, "display-attribute")))
        attribute_button = driver.find_element(By.CLASS_NAME, "display-attribute")
        driver.execute_script("arguments[0].scrollIntoView(true);", attribute_button)
        attribute_button.click()

        # Uncheck the required checkboxes
        wait = WebDriverWait(driver, timeout=10)
        wait.until(ec.visibility_of_element_located((By.ID, "roster-details-multi-checkbox")))
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "#roster-details-multi-checkbox div input")
        click = [0, 3, 5, 6, 7, 9, 10, 11, 12]
        for num in click:
            checkboxes[num].click()

        driver.find_element(By.ID, "roster-details-multi-checkbox-modal-submit-button").click()
        time.sleep(1)

    def extract_logins(self, driver):
        """Extracts the scheduled associate logins from the table."""
        wait_long = WebDriverWait(driver, timeout=60)
        wait_long.until(ec.visibility_of_element_located((By.CLASS_NAME, "display-attribute")))
        elements = driver.find_elements(By.CSS_SELECTOR, ".roster-details-table-body tr td")
        logins = set()
        for element in elements:
            if element.text != "":
                logins.add(element.text)
            else:
                break
        return logins
