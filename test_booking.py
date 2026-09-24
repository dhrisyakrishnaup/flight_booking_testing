import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

class TestExpediaFlight:
    def test_expedia_homepage(self, driver):
        driver.get("https://www.expedia.ae/")

        wait = WebDriverWait(driver, 20)

        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )
        print("Title:", driver.title)

    def check_bot_detection(self, driver):
        if (
                "Bot or Not?" in driver.title
                or "browsing and clicking at a speed" in driver.page_source
                or "Something is preventing JavaScript" in driver.page_source
        ):
            driver.save_screenshot("screenshots/bot_detection.png")
            print("Bot detection page appeared")
            print("Screenshot saved: screenshots/bot_detection.png")
            return True

        return False



    def test_flight_booking(self, driver):

        driver.get("https://www.expedia.ae/")

        wait = WebDriverWait(driver, 20)

        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )
        if self.check_bot_detection(driver):
            pytest.fail("Expedia bot detection page appeared")

     # Click Flights
        flights = wait.until(
        EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Flights']")
            )
        )
        flights.click()

        print("Flights clicked successfully")
        if self.check_bot_detection(driver):
            pytest.fail("Expedia bot detection appeared after clicking Flights")

    # Select Round trip
        round_trip = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Roundtrip']")
            )
        )
        round_trip.click()

        print("Round trip selected")
        driver.save_screenshot("screenshots/after_roundtrip.png")

        # Check bot detection after selecting Roundtrip
        if self.check_bot_detection(driver):
            pytest.fail(
                "Expedia bot detection appeared after selecting Roundtrip"
            )

    # Click Leaving from
        from_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "origin_select-input")
            )
        )

        from_button.click()
        print("Leaving from clicked successfully")

    # Get the same input using its ID
        airport_input = wait.until(
            EC.presence_of_element_located(
                (By.ID, "origin_select-input")
            )
        )

    # Type Dubai slowly
        airport_input.clear()

        for char in "Dubai":
            airport_input.send_keys(char)
            time.sleep(0.3)

        print("Dubai entered")

        # Wait briefly for autocomplete
        time.sleep(1)

        # Move through the dropdown options
        airport_input.send_keys(Keys.ARROW_DOWN)  # 1st option - DWC
        airport_input.send_keys(Keys.ARROW_DOWN)  # 2nd option - DXB All Airports
        airport_input.send_keys(Keys.ARROW_DOWN)  # 3rd option - DXB Dubai Intl.
        airport_input.send_keys(Keys.ENTER)

        print("Dubai International Airport selected")

        time.sleep(1)

        print(
            "Selected origin:",
            airport_input.get_attribute("value")
        )

        driver.save_screenshot(
            "screenshots/after_airport_selection.png"
        )

        # Click Going to
        to_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "destination_select-input")
            )
        )

        to_button.click()

        print("Going to clicked")

        destination_input = wait.until(
            EC.presence_of_element_located(
                (By.ID, "destination_select-input")
            )
        )

        destination_input.clear()

        for char in "London":
            destination_input.send_keys(char)
            time.sleep(0.3)

        print("London entered")

        time.sleep(1)

        destination_input.send_keys(Keys.ARROW_DOWN)
        destination_input.send_keys(Keys.ENTER)

        print("Destination selected")

        # Click Dates
        date_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "button[data-testid='uitk-date-selector-input1-default']"
                )
            )
        )

        # Check if calendar is already open
        if date_button.get_attribute("aria-expanded") != "true":
            date_button.click()

        print("Calendar opened")

        # Fixed dates
        departure_label = "Thursday, September 17, 2026"
        return_label = "Thursday, September 24, 2026"

        # Select departure date
        departure = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[contains(@class,'uitk-day-button')]/div[@aria-label='{departure_label}']/.."
                )
            )
        )

        departure.click()

        print("Departure date selected:", departure_label)

        # Give Expedia time to update the calendar
        time.sleep(1)

        # Select return date
        return_date_element = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='uitk-day-aria-label' and contains(@aria-label, 'September 24, 2026')]/parent::div"
                )
            )
        )

        return_date_element.click()

        print("Return date selected:", return_label)

        time.sleep(1)

        # Click Travelers
        traveler_button = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-stid='open-room-picker']")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            traveler_button
        )

        time.sleep(1)

        driver.execute_script(
            "arguments[0].click();",
            traveler_button
        )

        print("Traveler menu opened")

        # Verify 1 adult is selected
        adult_count = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//input[@aria-label='Adults']"
                )
            )
        )

        assert adult_count.get_attribute("value") == "1"

        print("Traveler count verified: 1 adult")

        driver.save_screenshot(
            "screenshots/traveler_menu.png"
        )
        time.sleep(1)
        # Click Search
        search_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "search_button")
            )
        )

        search_button.click()

        print("Search button clicked")

        # Wait for Expedia response
        time.sleep(5)

        # Check bot detection after clicking Search
        if self.check_bot_detection(driver):
            pytest.fail(
                "Expedia bot detection appeared after clicking Search"
            )

        print("Flight results page loaded successfully")

















