

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

# Click element
def click_element(driver, element):
    try:
        element.click()
        print("Clicked element")
    except Exception as e:
        print(f"Error clicking element: {e}")

# Input text
def input_text(element, text):
    try:
        element.clear()
        element.send_keys(text)
        print(f"Input text: {text}")
    except Exception as e:
        print(f"Error inputting text: {e}")

# Select radio button
def select_radio(element):
    try:
        if not element.is_selected():
            element.click()
        print("Radio selected")
    except Exception as e:
        print(f"Error selecting radio: {e}")

# Select dropdown by visible text
def select_dropdown_by_text(element, text):
    from selenium.webdriver.support.ui import Select
    try:
        select = Select(element)
        select.select_by_visible_text(text)
        print(f"Dropdown selected: {text}")
    except Exception as e:
        print(f"Error selecting dropdown: {e}")

# Select multiple options in multi-select
def select_multiple_options(element, options):
    from selenium.webdriver.support.ui import Select
    try:
        select = Select(element)
        for option in options:
            select.select_by_visible_text(option)
        print(f"Selected options: {options}")
    except Exception as e:
        print(f"Error selecting multiple options: {e}")

# Upload file
def upload_file(element, file_path):
    try:
        element.send_keys(file_path)
        print(f"File uploaded: {file_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Handle alert
def accept_alert(driver):
    try:
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert accepted")
    except Exception as e:
        print(f"Error accepting alert: {e}")

# Switch to iframe
def switch_to_iframe(driver, iframe_element):
    try:
        driver.switch_to.frame(iframe_element)
        print("Switched to iframe")
    except Exception as e:
        print(f"Error switching to iframe: {e}")

# Drag and drop
def drag_and_drop(driver, source, target):
    try:
        ActionChains(driver).drag_and_drop(source, target).perform()
        print("Drag and drop performed")
    except Exception as e:
        print(f"Error in drag and drop: {e}")

# Scroll to element
def scroll_to_element(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView();", element)
        print("Scrolled to element")
    except Exception as e:
        print(f"Error scrolling to element: {e}")

# Validate element text
def validate_text(element, expected_text):
    try:
        actual = element.text.strip()
        assert actual == expected_text, f"Expected '{expected_text}', got '{actual}'"
        print("Text validated")
    except Exception as e:
        print(f"Text validation failed: {e}")

# Take screenshot
def take_screenshot(driver, file_path):
    try:
        driver.save_screenshot(file_path)
        print(f"Screenshot saved: {file_path}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")

# Wait for element to be clickable
def wait_for_clickable(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        print("Element is clickable")
        return element
    except Exception as e:
        print(f"Element not clickable: {e}")
        return None

# Wait for element presence
def wait_for_presence(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        print("Element is present")
        return element
    except Exception as e:
        print(f"Element not present: {e}")
        return None

# Pick date (for input type="date")
def pick_date(element, date_str):
    try:
        element.clear()
        element.send_keys(date_str)
        print(f"Date set: {date_str}")
    except Exception as e:
        print(f"Error setting date: {e}")

# Hover over element
def hover_over_element(driver, element):
    try:
        ActionChains(driver).move_to_element(element).perform()
        print("Hovered over element")
    except Exception as e:
        print(f"Error hovering: {e}")

# Read table data
def get_table_data(table_element):
    try:
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data.append([col.text for col in cols])
        print("Table data extracted")
        return data
    except Exception as e:
        print(f"Error reading table: {e}")
        return []
