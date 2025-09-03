import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Import the required functions
from Framework.actions import set_date_range, parse_date_range, find_element_by_multiple_selectors, scroll_to_element

def test_date_range():
    """Test the date range picker functionality with different input formats"""
    # Setup WebDriver
    chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ChromeDriver.exe'))
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    
    # Define test date ranges in various formats
    test_date_ranges = [
        "08/15/2024-08/25/2024",
        "09/01/2024 to 09/10/2024",
        "Start: 10/05/2024, End: 10/15/2024",
        "11/01/2024 - 11/10/2024"
    ]
    
    try:
        # Open the test page
        driver.get("https://testautomationpractice.blogspot.com/")
        driver.maximize_window()
        print("Page loaded successfully")
        
        # Wait for page to load completely
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Scroll down to find the date range picker
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1)
        
        # Look for the date range picker section
        selectors = [
            (By.ID, "start-date"),
            (By.XPATH, "//label[contains(text(), 'Date Picker 3')]"),
            (By.XPATH, "//label[contains(text(), 'Date Range')]"),
            (By.XPATH, "//*[contains(text(), 'Select a Date Range')]")
        ]
        
        date_range_element = find_element_by_multiple_selectors(driver, selectors)
        
        if date_range_element:
            print("Date range picker section found")
            
            # Find the date range inputs
            section_parent = date_range_element.find_element(By.XPATH, "./parent::*")
            range_inputs = section_parent.find_elements(By.XPATH, ".//input[@placeholder='mm/dd/yyyy']")
            
            if len(range_inputs) >= 2:
                start_date_field = range_inputs[0]
                end_date_field = range_inputs[1]
                
                # Test each date range format
                for date_range_str in test_date_ranges:
                    print(f"\nTesting date range format: {date_range_str}")
                    
                    # Parse the date range
                    start_date, end_date = parse_date_range(date_range_str)
                    if start_date and end_date:
                        print(f"Parsed: {start_date} to {end_date}")
                        
                        # Set the date range
                        set_date_range(driver, start_date_field, end_date_field, start_date, end_date)
                        
                        # Wait to see the results
                        time.sleep(2)
                        
                        # Check for any output showing days or similar
                        try:
                            day_texts = driver.find_elements(By.XPATH, 
                                "//*[contains(text(), 'day') or contains(text(), 'Day') or contains(text(), 'selected')]")
                            if day_texts:
                                for element in day_texts:
                                    if element.is_displayed():
                                        print(f"Result text: {element.text}")
                        except:
                            pass
                    else:
                        print(f"Failed to parse date range: {date_range_str}")
            else:
                print("Could not find date input fields")
        else:
            print("Date range picker section not found")
            
            # Try fallback by looking for all date inputs
            all_date_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='mm/dd/yyyy' or contains(@class, 'date')]")
            print(f"Found {len(all_date_inputs)} date inputs total")
            
            # The date range picker should be the last 2 inputs (typically)
            if len(all_date_inputs) >= 4:  # Assuming we have datepicker1, datepicker2, and 2 for range
                start_date_field = all_date_inputs[-2]
                end_date_field = all_date_inputs[-1]
                
                # Scroll to these elements
                scroll_to_element(driver, start_date_field)
                time.sleep(1)
                
                # Test the last date range format as a fallback
                date_range_str = test_date_ranges[-1]
                start_date, end_date = parse_date_range(date_range_str)
                set_date_range(driver, start_date_field, end_date_field, start_date, end_date)
                print(f"Set date range using fallback: {start_date} to {end_date}")
            else:
                print("Not enough date inputs found for date range fallback test")
        
        # Take a screenshot of the final state
        screenshot_path = os.path.join(os.path.dirname(__file__), "date_range_test.png")
        driver.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved to: {screenshot_path}")
        
    except Exception as e:
        print(f"Test error: {e}")
    
    finally:
        # Close browser
        time.sleep(3)  # Wait to see results
        driver.quit()
        print("Test completed")

if __name__ == "__main__":
    test_date_range()
