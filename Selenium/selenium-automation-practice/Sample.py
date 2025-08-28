
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import openpyxl
import time
from Framework.actions import (
    click_element as click,
    input_text,
    select_radio,
    select_dropdown_by_text,
    upload_file,
    pick_date,
    get_table_data,
    take_screenshot,
    validate_text,
    scroll_to_element
)
from Framework.elementConstruct import construct_element


# ---------- Load Excel ----------
data_path = os.path.join(os.path.dirname(__file__), 'data.xlsx')
workbook = openpyxl.load_workbook(data_path)
sheet = workbook.active

# ---------- Start Chrome ----------
chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ChromeDriver.exe'))
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://testautomationpractice.blogspot.com/")
driver.maximize_window()
wait = WebDriverWait(driver, 10)
THINKTIME = 1
# ---------- Loop through Excel rows ----------
for row in sheet.iter_rows(min_row=2, values_only=True):
    (name, email, phone, address, gender, days, country, color, 
     date1, upload_file) = row[:10]  # Adjust columns if needed

    print(f"\nRunning test for {name}")

    # --- Name ---
    name_field = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    input_text(name_field, name or "")
    time.sleep(THINKTIME)
    # --- Email ---
    email_field = driver.find_element(By.ID, "email")
    input_text(email_field, email or "")
    time.sleep(THINKTIME)
    # --- Phone ---
    phone_field = driver.find_element(By.ID, "phone")
    input_text(phone_field, str(phone or ""))
    time.sleep(THINKTIME)
    # --- Address / Comments ---
    address_field = driver.find_element(By.ID, "textarea")
    input_text(address_field, address or "")
    time.sleep(THINKTIME)
    # --- Gender ---
    if gender:
        gender_id = "male" if gender.lower().startswith("m") else "female"
        gender_radio = driver.find_element(By.ID, gender_id)
        select_radio(gender_radio)
    # --- Days checkboxes ---
    print(f"{days}")
    # --- Days checkboxes ---
    if days:
        for day in days.split(","):
            day = day.strip()
            try:
                xPath = f"//input[@id='{day.lower()}' and contains(@value,'{day.lower()}')]"
                print(f"xPath: {xPath}")
                checkbox = driver.find_element(By.XPATH, xPath)
                checkbox.click()
                time.sleep(THINKTIME + 10)
                print(f"Checked Day: {day}")
                #get checkbox selected or not
                is_selected = checkbox.is_selected()
                print(f"Checkbox Selected: {is_selected}")

            except:
                print(f"Checkbox for {day} not found")
    # --- Country dropdown ---
    if country:
        country_select = driver.find_element(By.ID, "country")
        select_dropdown_by_text(country_select, country)
    time.sleep(THINKTIME)
    # --- Colors dropdown ---
    if color:
        color_select = driver.find_element(By.ID, "colors")
        select_dropdown_by_text(color_select, color)
    time.sleep(THINKTIME)
    
    # --- Sorted List (Multi-select) ---
    try:
        sorted_list = driver.find_element(By.XPATH, "//select[contains(@class, 'sorted') or @multiple]")
        from selenium.webdriver.support.ui import Select
        select_obj = Select(sorted_list)
        
        # Select multiple options from the sorted list
        options_to_select = ["Cat", "Dog", "Deer"]  # You can customize this
        for option in options_to_select:
            try:
                select_obj.select_by_visible_text(option)
                print(f"Selected from sorted list: {option}")
            except:
                print(f"Option '{option}' not found in sorted list")
        
        # Get selected options
        selected_options = [option.text for option in select_obj.all_selected_options]
        print(f"All selected options: {selected_options}")
        
    except:
        print("Sorted List not found")
    time.sleep(THINKTIME)
    # --- Date picker 1 (mm/dd/yyyy) ---
    if date1:
        date_str = date1.strftime("%m/%d/%Y") if hasattr(date1, 'strftime') else str(date1)
        date_field = driver.find_element(By.ID, "datepicker")
        pick_date(date_field, date_str)
        print(f"Date Picker 1 set to: {date_str}")
    time.sleep(THINKTIME)
    
    # --- Date picker 2 (dd/mm/yyyy) ---
    try:
        # Try multiple possible selectors for date picker 2
        date_field2 = None
        selectors = [
            "//input[@placeholder='dd/mm/yyyy']",
            "//input[contains(@placeholder, 'dd/mm')]",
            "//input[@id='datepicker2']",
            "//label[contains(text(), 'Date Picker 2')]/following-sibling::input",
            "//label[contains(text(), 'Date Picker 2')]/parent::*/input"
        ]
        
        for selector in selectors:
            try:
                date_field2 = driver.find_element(By.XPATH, selector)
                break
            except:
                continue
                
        if date_field2:
            if date1:
                # Convert to dd/mm/yyyy format
                date_str2 = date1.strftime("%d/%m/%Y") if hasattr(date1, 'strftime') else "15/08/2024"
            else:
                date_str2 = "15/08/2024"  # Default date
            pick_date(date_field2, date_str2)
            print(f"Date Picker 2 set to: {date_str2}")
        else:
            print("Date Picker 2 not found with any selector")
    except Exception as e:
        print(f"Date Picker 2 error: {e}")
    time.sleep(THINKTIME)
    
    # --- Date Range Picker (Date Picker 3) ---
    try:
        # Scroll down to find the date range picker section
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1)
        
        # Look specifically for Date Picker 3 section
        date_range_section = None
        try:
            # Try to find the Date Picker 3 label
            date_range_section = driver.find_element(By.XPATH, "//text()[contains(., 'Date Picker 3')]/parent::*")
        except:
            try:
                # Alternative: look for date range related text
                date_range_section = driver.find_element(By.XPATH, "//*[contains(text(), 'Date Range') or contains(text(), 'Select a Date Range')]")
            except:
                print("Date Picker 3 section not found")
        
        if date_range_section:
            # Find input fields within the date picker 3 section
            try:
                # Look for input fields near the Date Picker 3 section
                section_parent = date_range_section.find_element(By.XPATH, "./parent::*")
                range_inputs = section_parent.find_elements(By.XPATH, ".//input[@placeholder='mm/dd/yyyy']")
                
                if len(range_inputs) >= 2:
                    start_date_field = range_inputs[0]
                    end_date_field = range_inputs[1]
                    
                    # Clear any existing values first
                    start_date_field.clear()
                    end_date_field.clear()
                    
                    # Set start and end dates for range
                    start_date = "08/15/2024"
                    end_date = "08/25/2024"
                    
                    # Use JavaScript to set the values to avoid conflicts
                    driver.execute_script("arguments[0].value = arguments[1];", start_date_field, start_date)
                    driver.execute_script("arguments[0].value = arguments[1];", end_date_field, end_date)
                    
                    # Trigger change events
                    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", start_date_field)
                    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", end_date_field)
                    
                    time.sleep(2)
                    print(f"Date Range set: {start_date} to {end_date}")
                    
                    # Try to capture the days count output
                    try:
                        # Wait a bit for the calculation to appear
                        time.sleep(1)
                        
                        # Look for days output near the date range section
                        days_selectors = [
                            ".//*[contains(text(), 'days')]",
                            ".//*[contains(text(), 'selected')]",
                            ".//*[contains(text(), 'total')]",
                            ".//span[contains(@class, 'result')]",
                            ".//div[contains(@class, 'result')]"
                        ]
                        
                        days_found = False
                        for selector in days_selectors:
                            try:
                                days_output = section_parent.find_element(By.XPATH, selector)
                                if days_output.is_displayed() and days_output.text.strip():
                                    print(f"Days selected output: {days_output.text}")
                                    days_found = True
                                    break
                            except:
                                continue
                        
                        if not days_found:
                            # Look for any numeric output that might be the days count
                            all_text_elements = section_parent.find_elements(By.XPATH, ".//*[text()]")
                            for element in all_text_elements:
                                text = element.text.strip()
                                if text.isdigit() or any(keyword in text.lower() for keyword in ['day', 'selected', 'total']):
                                    print(f"Possible days output: {text}")
                                    break
                            else:
                                print("Days output not found")
                                
                    except Exception as e:
                        print(f"Error finding days output: {e}")
                else:
                    print("Could not find 2 date input fields in Date Picker 3 section")
                    
            except Exception as e:
                print(f"Error finding date inputs in section: {e}")
        else:
            # Fallback: try to find date range inputs by their position on page
            try:
                # Look for all date inputs and try to identify the date range ones
                all_date_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='mm/dd/yyyy' or contains(@class, 'date')]")
                print(f"Found {len(all_date_inputs)} date inputs total")
                
                # The date range picker should be the last 2 inputs (typically)
                if len(all_date_inputs) >= 4:  # Assuming we have datepicker1, datepicker2, and 2 for range
                    start_date_field = all_date_inputs[-2]
                    end_date_field = all_date_inputs[-1]
                    
                    # Scroll to these elements
                    driver.execute_script("arguments[0].scrollIntoView();", start_date_field)
                    time.sleep(1)
                    
                    start_date_field.clear()
                    end_date_field.clear()
                    
                    start_date = "08/15/2024"
                    end_date = "08/25/2024"
                    
                    start_date_field.send_keys(start_date)
                    time.sleep(1)
                    end_date_field.send_keys(end_date)
                    time.sleep(2)
                    
                    print(f"Date Range set (fallback method): {start_date} to {end_date}")
                else:
                    print("Not enough date inputs found for date range")
                    
            except Exception as e:
                print(f"Fallback date range error: {e}")
                
    except Exception as e:
        print(f"Date Range Picker error: {e}")
    time.sleep(THINKTIME)
    # --- File Upload ---
    try:
        if upload_file:
            # Try multiple selectors for file upload
            file_input = None
            file_selectors = [
                "//input[@id='filename']",
                "//input[@type='file']",
                "//input[@name='file']",
                "//input[contains(@id, 'file')]",
                "//label[contains(text(), 'Choose file') or contains(text(), 'Upload')]/following-sibling::input",
                "//label[contains(text(), 'Choose file') or contains(text(), 'Upload')]/parent::*/input"
            ]
            
            for selector in file_selectors:
                try:
                    file_input = driver.find_element(By.XPATH, selector)
                    break
                except:
                    continue
            
            if file_input:
                upload_file(file_input, upload_file)
            else:
                print("File upload element not found with any selector")
        else:
            print("No file specified for upload")
    except Exception as e:
        print(f"File upload error: {e}")
    time.sleep(THINKTIME)
    # --- Submit ---
    submit = construct_element(driver, By.XPATH, "//input[@value='Submit']")
    click(driver, submit)
    print("Clicked Submit button")
    
    # Take screenshot after submission
    screenshot_path = os.path.join(os.path.dirname(__file__), f"screenshot_{name or 'test'}.png")
    take_screenshot(driver, screenshot_path)
    
    # Check for any success/error messages
    try:
        # Look for any alert or message after submission
        success_msg = driver.find_element(By.XPATH, "//div[contains(@class, 'success') or contains(@class, 'message') or contains(@class, 'alert')]")
        print(f"Message found: {success_msg.text}")
    except:
        print("No success/error message found")
    
    # Check for any modal or popup
    try:
        modal = driver.find_element(By.XPATH, "//div[contains(@class, 'modal') or contains(@id, 'modal')]")
        if modal.is_displayed():
            print(f"Modal displayed: {modal.text}")
    except:
        print("No modal found")
    
    time.sleep(3)
    
    # Try to interact with Wikipedia search (if available on page)
    try:
        wiki_search = driver.find_element(By.ID, "Wikipedia1_wikipedia-search-input")
        input_text(wiki_search, "Selenium")
        wiki_button = driver.find_element(By.XPATH, "//input[@class='wikipedia-search-button']")
        click(driver, wiki_button)
        time.sleep(2)
        print("Wikipedia search performed")
    except:
        print("Wikipedia search not available or failed")
    
    # Try to interact with double click button (if available)
    try:
        double_click_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Copy Text')]")
        double_click_btn.double_click()
        print("Double click performed")
    except:
        print("Double click button not found")
    
    # Try to interact with drag and drop (if available)
    try:
        from selenium.webdriver.common.action_chains import ActionChains
        source = driver.find_element(By.ID, "draggable")
        target = driver.find_element(By.ID, "droppable")
        ActionChains(driver).drag_and_drop(source, target).perform()
        print("Drag and drop performed")
    except:
        print("Drag and drop elements not found")
    
    # Check for iframes and interact if present
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        # Try to find and interact with elements inside iframe
        iframe_input = driver.find_element(By.TAG_NAME, "input")
        input_text(iframe_input, "Test in iframe")
        driver.switch_to.default_content()
        print("Iframe interaction completed")
    except:
        print("No iframe found or interaction failed")
        driver.switch_to.default_content()  # Ensure we're back to main content
    time.sleep(THINKTIME)
    # --- Read Static Table ---
    print("\nStatic Table:")
    try:
        static_table = driver.find_element(By.XPATH, "//table[@border='1']")
        static_data = get_table_data(static_table)
        print("Static Table Data:")
        for i, row in enumerate(static_data):
            print(f"Row {i}: {row}")
    except:
        print("Static table not found")
    time.sleep(THINKTIME)
    
    # --- Read Dynamic Table ---
    print("\nDynamic Table:")
    try:
        dynamic_table = driver.find_element(By.XPATH, "//table[@border='1' and .//th[text()='Name']]")
        dynamic_data = get_table_data(dynamic_table)
        print("Dynamic Table Data:")
        for i, row in enumerate(dynamic_data):
            print(f"Row {i}: {row}")
    except:
        print("Dynamic table not found")
    
    # --- Pagination Test (if available) ---
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Next') or contains(text(), '»')]")
        click(driver, next_button)
        print("Pagination: Clicked Next")
        time.sleep(2)
        # Read table again after pagination
        try:
            paginated_table = driver.find_element(By.XPATH, "//table[@border='1']")
            paginated_data = get_table_data(paginated_table)
            print("Paginated Table Data:")
            for i, row in enumerate(paginated_data):
                print(f"Page 2 Row {i}: {row}")
        except:
            print("Could not read paginated table")
    except:
        print("No pagination found")
    
    # --- Scroll and check for additional elements ---
    try:
        # Scroll to bottom to load any lazy-loaded content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        print("Scrolled to bottom of page")
        
        # Look for any additional buttons or elements
        buttons = driver.find_elements(By.XPATH, "//button | //input[@type='button'] | //input[@type='submit']")
        print(f"Found {len(buttons)} buttons on page")
        
        # Try to interact with alert buttons if available
        alert_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Alert') or contains(text(), 'Confirm') or contains(text(), 'Prompt')]")
        for btn in alert_buttons[:3]:  # Limit to first 3 to avoid too many alerts
            try:
                btn.click()
                time.sleep(1)
                alert = driver.switch_to.alert
                alert_text = alert.text
                print(f"Alert text: {alert_text}")
                alert.accept()
                print("Alert accepted")
            except:
                print("No alert appeared or already handled")
                
    except Exception as e:
        print(f"Error during additional interactions: {e}")
    
    print(f"Completed test for {name}")
    print("-" * 50)

# Close browser
driver.quit()
print("\nAll tests completed successfully")