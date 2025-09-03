import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Import necessary functions from actions module
from Framework.actions import get_table_data, get_text_below_element

def test_dynamic_table():
    """Test the dynamic table functionality on the test automation practice site"""
    # Setup WebDriver
    chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ChromeDriver.exe'))
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        # Open the test page
        driver.get("https://testautomationpractice.blogspot.com/")
        driver.maximize_window()
        print("Page loaded successfully")
        
        # Wait for page to load completely
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Scroll to the Dynamic Web Table section
        try:
            table_header = driver.find_element(By.XPATH, "//h2[contains(text(),'Dynamic Web Table')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", table_header)
            time.sleep(1)  # Wait for scroll to complete
            print("Scrolled to Dynamic Web Table section")
        except Exception as scroll_error:
            print(f"Could not scroll to Dynamic Web Table: {scroll_error}")
        
        # Try multiple approaches to find the table
        table_locators = [
            (By.ID, "taskTable"),
            (By.XPATH, "//div[contains(@class, 'widget-content')]//table"),
            (By.CSS_SELECTOR, "div.widget-content table"),
            (By.XPATH, "//table[.//th[contains(text(), 'Name')]]")
        ]
        
        dynamic_table = None
        for locator_type, locator in table_locators:
            try:
                dynamic_table = driver.find_element(locator_type, locator)
                print(f"Found dynamic table using {locator_type}: {locator}")
                break
            except Exception:
                continue
        
        if dynamic_table:
            # Extract table data
            table_data = get_table_data(dynamic_table)
            
            # Print header and top three rows
            print("\n=== TOP 3 ROWS FROM DYNAMIC TABLE ===")
            for i, row in enumerate(table_data[:4]):  # Header + 3 rows
                if i == 0:
                    print(f"Header: {' | '.join(str(cell) for cell in row)}")
                    print("-" * 60)
                else:
                    print(f"Row {i}: {' | '.join(str(cell) for cell in row)}")
            
            print(f"\nTotal rows in dynamic table: {len(table_data)}")
            
            # Extract text below the table
            print("\n=== TEXT BELOW DYNAMIC TABLE ===")
            
            # Try by ID first
            try:
                display_values = driver.find_element(By.ID, "displayValues")
                if display_values:
                    print(f"Display Values content:\n{display_values.text}")
            except Exception:
                # Try using our custom function
                below_table_text = get_text_below_element(driver, dynamic_table, "div.display-values, #displayValues")
                if below_table_text:
                    for i, text in enumerate(below_table_text):
                        print(f"Text {i+1}: {text}")
                else:
                    # Last resort: get all text after the table using XPath
                    try:
                        text_elements = driver.find_elements(By.XPATH, 
                            "//table/following::div[contains(text(), 'CPU') or contains(text(), 'Memory') or contains(text(), 'Network') or contains(text(), 'Disk')]")
                        if text_elements:
                            print("Found text elements below table:")
                            for elem in text_elements:
                                print(elem.text)
                        else:
                            print("No text elements found below table with specific content")
                    except Exception as e:
                        print(f"Could not find text below table: {e}")
            
            # Take a screenshot showing the table and text
            screenshot_path = os.path.join(os.path.dirname(__file__), "dynamic_table_screenshot.png")
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved to: {screenshot_path}")
        else:
            print("Dynamic table not found with any of the locators")
    
    except Exception as e:
        print(f"Test error: {e}")
    
    finally:
        # Close browser
        time.sleep(3)  # Wait to see results
        driver.quit()
        print("Test completed")

if __name__ == "__main__":
    test_dynamic_table()
