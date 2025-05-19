import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.check_dates import compare_dates

magic_keys = ["inspire-key-pass", "beleive-key-pass", "enchant-key-pass", "imagine-key-pass"]

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36")
service = Service(ChromeDriverManager().install())

def expand_shadow_element(driver, element):
    """ Expands shadow DOM layers and returns the shadow root. """
    return driver.execute_script("return arguments[0].shadowRoot", element)

def fetch_all_dates(key_id):
    """ Fetch availability for dates within the next 90 days for the given Magic Key. """
    try:
        print(f"Fetching page content for key: {key_id} using Selenium...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://disneyland.disney.go.com/passes/blockout-dates/")

        # Wait for the main container to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "com-park-admission-calendar-pass-selection"))
        )

        # Access the shadow DOM structure
        pass_selection = driver.find_element(By.CSS_SELECTOR, "com-park-admission-calendar-pass-selection")
        shadow_root_1 = expand_shadow_element(driver, pass_selection)

        # Find the button within shadow DOM by its ID
        button = shadow_root_1.find_element(By.CSS_SELECTOR, f"com-button#{key_id}")

        # Scroll to the button to make it visible and click
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth' });", button)
        time.sleep(1)

        is_selected = button.get_attribute("aria-pressed") == "true"
        if not is_selected:
            button.click()
            time.sleep(1)

        # Wait for the calendar container to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "com-park-admission-calendar-container"))
        )

        # Access the shadow DOM for the calendar container
        calendar_container = driver.find_element(By.CSS_SELECTOR, "com-park-admission-calendar-container")
        shadow_root_calendar = expand_shadow_element(driver, calendar_container)

        # Access the admission calendar shadow DOM
        admission_calendar = shadow_root_calendar.find_element(By.CSS_SELECTOR, "#admissionCalendar")
        shadow_root_admission_calendar = expand_shadow_element(driver, admission_calendar)

        # Date filtering setup
        current_date = datetime.now()
        ninety_days_from_now = current_date + timedelta(days=90)

        # Extract all dates and their statuses
        dates_data = {}
        date_elements = shadow_root_admission_calendar.find_elements(By.CSS_SELECTOR, "div[slot]")

        for date_element in date_elements:
            slot = date_element.get_attribute("slot")
            try:
                slot_date = datetime.strptime(slot, "%Y-%m-%d")
                # Only include dates within the next 90 days
                if current_date <= slot_date <= ninety_days_from_now:
                    aria_label = date_element.get_attribute("aria-label")
                    css_class = date_element.get_attribute("class")

                    if "Either Park Available" in aria_label or "all" in css_class:
                        availability_status = "Both Parks Available"
                    elif "Disneyland Park Available" in aria_label or "primary" in css_class:
                        availability_status = "Disneyland Only Available"
                    elif "Disney California Adventure Park Available" in aria_label or "secondary" in css_class:
                        availability_status = "California Adventure Only Available"
                    elif "No Magic Key Reservations Available" in aria_label or "ternary" in css_class:
                        availability_status = "Unavailable"
                    else:
                        availability_status = "Unknown"

                    dates_data[slot] = availability_status

            except ValueError:
                pass  # Skip dates that don't follow the expected format

        return dates_data

    except Exception as e:
        print(f"Error fetching data for key {key_id}: {e}")
        return {}

    finally:
        driver.quit()

def check_reservations(keys):
    print(f"Checking reservations at {datetime.now()}")
    for key in keys:
        print(f"Starting scraping process for {key}...")
        availability_data = fetch_all_dates(key)
        compare_dates(availability_data, key)

        print(f"Scraping completed. Data collected for {key}: {availability_data}")
    # return availability_data