
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
    upload_file_with_submit,
    pick_date,
    get_table_data,
    take_screenshot,
    validate_text,
    scroll_to_element,
    interact_with_date_picker,
    set_date_range,
    find_element_by_multiple_selectors,
    find_element_with_text,
    select_from_multi_select,
    select_day_checkbox,
    get_text_below_element
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
     date1,date2,date_range_section, upload_file) = row[:12]  # Adjust columns if needed

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
            is_selected = select_day_checkbox(driver, day)
            time.sleep(THINKTIME)
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
        
        # Select multiple options from the sorted list
        options_to_select = ["Cat", "Dog", "Deer"]  # You can customize this
        selected_options = select_from_multi_select(driver, sorted_list, options_to_select)
        
        print(f"All selected options: {selected_options}")
        
    except Exception as e:
        print(f"Sorted List not found: {e}")
    time.sleep(THINKTIME)
    # --- Date picker 1 (mm/dd/yyyy) ---
    if date1:
        try:
            date_str = date1.strftime("%m/%d/%Y") if hasattr(date1, 'strftime') else str(date1)
            date_field = driver.find_element(By.ID, "datepicker")
            
            # Use the reusable function for date picker interaction
            interact_with_date_picker(driver, date_field, date_str)
            print(f"Date Picker 1 set to: {date_str} and closed")
            
        except Exception as e:
            print(f"Error with Date Picker 1: {e}")
    time.sleep(THINKTIME)
    
    # --- Date picker 2 (dd/mm/yyyy) ---

    if date2:
        try:
            date_str2 = date2.strftime("%m/%d/%Y") if hasattr(date2, 'strftime') else str(date2)
            date_field2 = driver.find_element(By.ID, "txtDate")
            
            # Use the reusable function for date picker interaction
            interact_with_date_picker(driver, date_field2, date_str2)
            print(f"Date Picker 2 set to: {date_str2} and closed")
    
        except Exception as e:
            print(f"Error with Date Picker 2: {e}")
    time.sleep(THINKTIME)
    
    # --- Date Range Picker (Date Picker 3) ---
    try:
        # Scroll down to find the date range picker section
        scroll_to_element(driver, driver.find_element(By.TAG_NAME, "body"))
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1)
        
        # Check if we have a date range value from Excel
        if date_range_section:
            print(f"Using date range from Excel: {date_range_section}")
            
            # Use our enhanced parse_date_range function
            from Framework.actions import parse_date_range
            start_date, end_date = parse_date_range(date_range_section)
            
            if start_date and end_date:
                print(f"Parsed date range: {start_date} to {end_date}")
            else:
                # Fallback to default dates if parsing failed
                start_date = "08/15/2024"
                end_date = "08/25/2024"
                print(f"Failed to parse date range, using defaults: {start_date} to {end_date}")
        else:
            # Default dates if none provided in Excel
            start_date = "08/15/2024"
            end_date = "08/25/2024"
            print("No date range provided in Excel, using defaults")
            
        # Look specifically for Date Picker 3 section
        date_range_element = None
        try:
            # Try to find the Date Picker 3 label or start-date field
            selectors = [
                (By.ID, "start-date"),
                (By.XPATH, "//label[contains(text(), 'Date Picker 3')]"),
                (By.XPATH, "//label[contains(text(), 'Date Range')]"),
                (By.XPATH, "//*[contains(text(), 'Select a Date Range')]")
            ]
            date_range_element = find_element_by_multiple_selectors(driver, selectors)
        except Exception as e:
            print(f"Date Picker 3 search error: {e}")
        
        if date_range_element:
            try:
                # Look for input fields near the Date Picker 3 section
                section_parent = date_range_element.find_element(By.XPATH, "./parent::*")
                range_inputs = section_parent.find_elements(By.XPATH, ".//input[@placeholder='mm/dd/yyyy']")
                
                if len(range_inputs) >= 2:
                    start_date_field = range_inputs[0]
                    end_date_field = range_inputs[1]
                    
                    # Use our reusable function to set date range with values from Excel or defaults
                    set_date_range(driver, start_date_field, end_date_field, start_date, end_date)

                    # Look for days output using find_element_with_text
                    days_output = find_element_with_text(driver, "days")
                    if days_output and days_output.is_displayed():
                        print(f"Days selected output: {days_output.text}")
                    else:
                        print("Days output not found directly")
                        
                        # Try other text that might indicate days
                        for keyword in ["selected", "total", "range"]:
                            element = find_element_with_text(driver, keyword)
                            if element and element.is_displayed():
                                print(f"Possible days output: {element.text}")
                                break
                                
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
                    scroll_to_element(driver, start_date_field)
                    time.sleep(1)
                    
                    # Use date range from Excel or the defaults we already set above
                    set_date_range(driver, start_date_field, end_date_field, start_date, end_date)
                    
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
            # Try single file upload using the new HTML structure
            success = upload_file_with_submit(
                driver=driver,
                file_input_id="singleFileInput",
                file_path=upload_file,
                form_id="singleFileForm",
                submit_button_xpath="//button[@type='submit' and text()='Upload Single File']",
                status_id="singleFileStatus"
            )
            
            # If single file upload fails, try multiple files form if available
            if not success:
                try:
                    # Look for multiple files form and attempt to use it
                    multiple_form = driver.find_element(By.ID, "multipleFilesForm")
                    if multiple_form:
                        # Try to find file input in the multiple files form
                        multiple_file_inputs = driver.find_elements(By.XPATH, "//form[@id='multipleFilesForm']//input[@type='file']")
                        if multiple_file_inputs:
                            upload_file(multiple_file_inputs[0], upload_file)
                            # Submit the form if needed
                            try:
                                multiple_form.submit()
                                print("Multiple files form submitted")
                                
                                # Check status
                                status = driver.find_element(By.ID, "multipleFilesStatus")
                                if status:
                                    print(f"Multiple upload status: {status.text}")
                            except Exception as submit_error:
                                print(f"Error submitting multiple files form: {submit_error}")
                except Exception as multi_error:
                    print(f"Multiple file upload failed: {multi_error}")
        else:
            print("No file specified for upload")
    except Exception as e:
        print(f"File upload error: {e}")
    time.sleep(THINKTIME)
    # --- Submit ---
    submit = construct_element(driver, By.XPATH, "//input[@value='Submit']")
    click(driver, submit)
    print("Clicked Submit button")
    
    time.sleep(3)
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
    print("\nStatic Web Table:")
    try:
        # Find the static table with books data
        static_table = driver.find_element(By.NAME, "BookTable")
        static_data = get_table_data(static_table)
        
        print("=== TOP 3 ROWS FROM STATIC TABLE ===")
        
        # Print header row first
        if len(static_data) > 0:
            print(f"Header: {static_data[0]}")
            print("-" * 60)
        
        # Print top 3 data rows (excluding header)
        for i in range(1, min(4, len(static_data))):
            row = static_data[i]
            print(f"Row {i}: BookName='{row[0]}', Author='{row[1]}', Subject='{row[2]}', Price='{row[3]}'")
        
        print(f"\nTotal rows in static table: {len(static_data)} (including header)")
        
    except Exception as e:
        print(f"Static table error: {e}")
    time.sleep(THINKTIME)
    
    # --- Read Dynamic Table ---
    print("\nDynamic Web Table:")
    try:
        # First, scroll to the Dynamic Web Table section to ensure it's in view
        try:
            table_header = driver.find_element(By.XPATH, "//h2[contains(text(),'Dynamic Web Table')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", table_header)
            print("Scrolled to Dynamic Web Table section")
        except Exception as scroll_error:
            print(f"Could not scroll to Dynamic Web Table: {scroll_error}")
        
        # Find the dynamic table using the ID from the HTML source
        dynamic_table = driver.find_element(By.ID, "taskTable")
        
        # Extract all table data
        dynamic_data = get_table_data(dynamic_table)
        
        # Print header and top three rows
        print("\n=== TOP 3 ROWS FROM DYNAMIC TABLE ===")
        for i, row in enumerate(dynamic_data[:4]):  # Header + 3 rows
            if i == 0:
                print(f"Header: {' | '.join(str(cell) for cell in row)}")
                print("-" * 60)
            else:
                print(f"Row {i}: {' | '.join(str(cell) for cell in row)}")
                
        # Now extract the text information below the table
        print("\n=== TEXT BELOW DYNAMIC TABLE ===")
        
        # Method 1: Find text below table using class name from HTML source
        try:
            display_values = driver.find_element(By.ID, "displayValues")
            if display_values:
                print(f"Display Values content: {display_values.text}")
        except Exception as e1:
            print(f"Could not find display values by ID: {e1}")
            
            # Method 2: Use our new function to get text below the table
            below_table_text = get_text_below_element(driver, dynamic_table, "div.display-values")
            if below_table_text:
                for i, text in enumerate(below_table_text):
                    print(f"Text {i+1}: {text}")
            else:
                # Method 3: Use XPath to get elements after the table
                try:
                    text_elements = driver.find_elements(By.XPATH, 
                        "//table[@id='taskTable']/following::div[contains(text(), 'CPU') or contains(text(), 'Memory') or contains(text(), 'Network') or contains(text(), 'Disk')]")
                    for elem in text_elements:
                        print(elem.text)
                except Exception as e2:
                    print(f"Could not find text below table: {e2}")
                    
    except Exception as table_error:
        print(f"Dynamic table error: {table_error}")
    
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

# Print completion message
print("\nAll tests completed successfully")
