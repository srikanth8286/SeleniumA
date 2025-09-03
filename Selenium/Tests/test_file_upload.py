import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Import the enhanced upload function
from Framework.actions import upload_file_with_submit

# File to upload - adjust the path as needed
test_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'file1.txt'))

# Setup WebDriver
chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ChromeDriver.exe'))
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

try:
    # Navigate to the test page
    driver.get("https://testautomationpractice.blogspot.com/")
    driver.maximize_window()
    print("Page loaded successfully")

    # Test file upload with new function
    print(f"Testing file upload with {test_file_path}")
    
    # Scroll to the file upload section
    try:
        upload_header = driver.find_element(By.XPATH, "//h2[contains(text(), 'Upload Files')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", upload_header)
        print("Scrolled to Upload Files section")
    except Exception as e:
        print(f"Could not find Upload Files section: {e}")
    
    # Wait for elements to be visible
    time.sleep(2)
    
    # Attempt file upload
    success = upload_file_with_submit(
        driver=driver,
        file_input_id="singleFileInput",
        file_path=test_file_path,
        form_id="singleFileForm",
        submit_button_xpath="//button[@type='submit' and text()='Upload Single File']",
        status_id="singleFileStatus"
    )
    
    if success:
        print("File upload test succeeded!")
    else:
        print("File upload test failed!")
        
    # Take a screenshot
    screenshot_path = os.path.join(os.path.dirname(__file__), "upload_test_result.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")
    
except Exception as e:
    print(f"Test error: {e}")
finally:
    # Close the browser
    time.sleep(3)  # Wait to see results
    driver.quit()
    print("Test completed")
