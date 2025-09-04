
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
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
        sorted_list = driver.find_element(By.XPATH, "//*[@id='animals']")
        
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
    
    # --- Date picker 2 (dd/mm/yyyy), select it and click on the date ---

    if date2:
        try:
            date_str2 = date2.strftime("%d/%m/%Y") if hasattr(date2, 'strftime') else str(date2)
            date_field2 = driver.find_element(By.XPATH, "//*[@id='txtDate']")
            
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
            print("\n=== FILE UPLOAD TEST ===")
            
            # First, find and scroll to the upload section
            try:
                upload_section = driver.find_element(By.XPATH, "//h2[contains(text(), 'Upload') and contains(text(), 'Files')] | //div[contains(text(), 'Upload') and contains(text(), 'Files')]")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", upload_section)
                print("Scrolled to file upload section")
                time.sleep(2)  # Wait for scrolling to complete
            except Exception as scroll_error:
                print(f"Couldn't find upload section, will try anyway: {scroll_error}")
                
            # Single File Upload - Using more flexible approaches to find elements
            try:
                # Find file input using various selectors
                single_file_input = None
                possible_selectors = [
                    By.ID, "singleFileInput", 
                    By.XPATH, "//input[@type='file' and not(@multiple)]",
                    By.XPATH, "//form[contains(@id, 'single') or contains(@class, 'single')]//input[@type='file']",
                    By.XPATH, "//input[@type='file'][1]",  # Try first file input as fallback
                ]
                
                for i in range(0, len(possible_selectors), 2):
                    try:
                        single_file_input = driver.find_element(possible_selectors[i], possible_selectors[i+1])
                        print(f"Found single file input using selector: {possible_selectors[i+1]}")
                        break
                    except:
                        continue
                
                if single_file_input:
                    # Upload file directly using send_keys
                    single_file_input.send_keys(upload_file)
                    print(f"File selected for single upload: {upload_file}")
                    time.sleep(1)
                    
                    # Try to find and click the submit button
                    try:
                        # Try multiple approaches to find the submit button
                        submit_found = False
                        submit_selectors = [
                            "//button[contains(text(), 'Upload') and contains(text(), 'Single')]",
                            "//button[contains(text(), 'Upload') and contains(@type, 'submit')]",
                            "//input[@type='submit']",
                            f"//form[contains(.//input[@type='file']/@id, '{single_file_input.get_attribute('id')}')]//button",
                            "//button[contains(text(), 'Upload')]"
                        ]
                        
                        for selector in submit_selectors:
                            try:
                                submit_btn = driver.find_element(By.XPATH, selector)
                                submit_btn.click()
                                print(f"Clicked submit button found with: {selector}")
                                submit_found = True
                                break
                            except:
                                continue
                                
                        if not submit_found:
                            # Try to submit the form directly if we can find it
                            try:
                                parent_form = driver.execute_script("return arguments[0].form", single_file_input)
                                if parent_form:
                                    parent_form.submit()
                                    print("Submitted form directly")
                                    submit_found = True
                            except Exception as form_error:
                                print(f"Could not submit form: {form_error}")
                                
                        if submit_found:
                            print("Single file upload submitted")
                            time.sleep(2)  # Wait for potential status update
                    except Exception as submit_error:
                        print(f"Error submitting single file: {submit_error}")
                else:
                    print("Could not find single file input element")
            except Exception as e:
                print(f"Single file upload failed: {e}")
            
            # Multiple File Upload with similar flexible approach
            try:
                # Find multiple file input
                multiple_file_input = None
                possible_multi_selectors = [
                    By.ID, "multipleFilesInput",
                    By.XPATH, "//input[@type='file' and @multiple]",
                    By.XPATH, "//form[contains(@id, 'multiple') or contains(@class, 'multiple')]//input[@type='file']",
                    By.XPATH, "(//input[@type='file'])[2]",  # Try second file input as fallback
                ]
                
                for i in range(0, len(possible_multi_selectors), 2):
                    try:
                        multiple_file_input = driver.find_element(possible_multi_selectors[i], possible_multi_selectors[i+1])
                        print(f"Found multiple file input using selector: {possible_multi_selectors[i+1]}")
                        break
                    except:
                        continue
                
                if multiple_file_input:
                    # Upload file
                    multiple_file_input.send_keys(upload_file)
                    print(f"File selected for multiple upload: {upload_file}")
                    time.sleep(1)
                    
                    # Find and click submit button with similar flexible approach
                    try:
                        # Try multiple approaches to find the submit button
                        submit_found = False
                        multi_submit_selectors = [
                            "//button[contains(text(), 'Upload') and contains(text(), 'Multiple')]",
                            "//form[contains(@id, 'multiple')]//button[@type='submit']",
                            f"//form[contains(.//input[@type='file']/@id, '{multiple_file_input.get_attribute('id')}')]//button",
                        ]
                        
                        for selector in multi_submit_selectors:
                            try:
                                multi_submit = driver.find_element(By.XPATH, selector)
                                multi_submit.click()
                                print(f"Clicked multiple submit button found with: {selector}")
                                submit_found = True
                                break
                            except:
                                continue
                                
                        if not submit_found:
                            # Try to submit the form directly
                            try:
                                parent_form = driver.execute_script("return arguments[0].form", multiple_file_input)
                                if parent_form:
                                    parent_form.submit()
                                    print("Submitted multiple form directly")
                            except Exception as form_error:
                                print(f"Could not submit multiple form: {form_error}")
                                
                        print("Multiple files upload submitted")
                        time.sleep(2)  # Wait for status update
                    except Exception as multi_submit_error:
                        print(f"Error submitting multiple files: {multi_submit_error}")
                else:
                    print("Could not find multiple file input element")
            except Exception as e:
                print(f"Multiple files upload failed: {e}")
        else:
            print("No file specified for upload")
    except Exception as e:
        print(f"File upload error: {e}")
    time.sleep(THINKTIME)
    
    
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
    
    # Try to interact with Wikipedia search 
    try:
        wiki_search = driver.find_element(By.ID, "Wikipedia1_wikipedia-search-input")
        input_text(wiki_search, "Selenium")
        wiki_button = driver.find_element(By.XPATH, "//input[@class='wikipedia-search-button']")
        click(driver, wiki_button)
        time.sleep(2)
        print("Wikipedia search performed")
    except:
        print("Wikipedia search not available or failed")

    # try intereacting with dynamic button before clicking it is start and after clicking it is stop
    dynamic_button = driver.find_element(By.XPATH, "//*[@id='HTML5']/div[1]/button")
    ActionChains(driver).move_to_element(dynamic_button).perform()
    time.sleep(1)
    click(driver, dynamic_button)
    print("Dynamic button clicked-START TO STOP")
    time.sleep(1)

    # Try to interact with double click button 
    try:
        double_click_btn = driver.find_element(By.XPATH, "//*[@id='HTML10']/div[1]/button")
        ActionChains(driver).double_click(double_click_btn).double_click().perform()
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
    
    #new tab button click and close the new tab
    
    try:
        new_tab_btn = driver.find_element(By.XPATH, "//*[@id='HTML4']/div[1]/button")
        click(driver, new_tab_btn)
        print("New tab button clicked")
    except:
        print("New tab button not found")

    # popup window button click
    try:
        popup_btn = driver.find_element(By.XPATH, "//*[@id='PopUp']")
        click(driver, popup_btn)
        print("Popup window button clicked")
    except:
        print("Popup window button not found")

    # scrolling a dropdown and selecting an option
    try:
        dropdown = driver.find_element(By.XPATH, "//*[@id='comboBox']")
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
        print("Scrolled to dropdown")
        # Select an option from the dropdown
        select = Select(dropdown)
        select.select_by_visible_text("Item 10")
        print("Selected option from dropdown")
    except Exception as e:
        print(f"Error scrolling to dropdown: {e}")
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
                    text_elements = driver.find_elements(By.XPATH, "//*[@id='displayValues']")
                     #   "//table[@id='taskTable']/following::div[contains(text(), 'CPU') or contains(text(), 'Memory') or contains(text(), 'Network') or contains(text(), 'Disk')]")
                    for elem in text_elements:
                        print(elem.text)
                except Exception as e2:
                    print(f"Could not find text below table: {e2}")
                    
    except Exception as table_error:
        print(f"Dynamic table error: {table_error}")

    # --- Pagination Test  ---
    try:
        print("\n=== PAGINATION TABLE TEST ===")
        
        # Find the pagination table using its ID
        pagination_table = driver.find_element(By.ID, "productTable")
        print("Found pagination table with ID: productTable")
        
        # First select checkboxes from the first page
        checkboxes = pagination_table.find_elements(By.XPATH, ".//tbody//input[@type='checkbox']")
        if checkboxes:
            # Select the first item
            if len(checkboxes) >= 1:
                checkboxes[0].click()
                print("Selected item #1 from pagination table")
            
            # Select the third item 
            if len(checkboxes) >= 3:
                checkboxes[2].click()
                print("Selected item #3 from pagination table")
        
        time.sleep(1)
        
        # Find and click on page 2 button using the pagination element
        pagination_element = driver.find_element(By.ID, "pagination")
        page2_link = pagination_element.find_element(By.XPATH, ".//li/a[text()='2']")
        click(driver, page2_link)
        print("Pagination: Clicked on Page 2")
        time.sleep(2)
        
        # Select items from page 2 (table remains the same but content changes)
        page2_checkboxes = pagination_table.find_elements(By.XPATH, ".//tbody//input[@type='checkbox']")
        if page2_checkboxes and len(page2_checkboxes) >= 1:
            page2_checkboxes[0].click()
            print("Selected first item from page 2")
            
        # Navigate to page 3
        page3_link = pagination_element.find_element(By.XPATH, ".//li/a[text()='3']")
        click(driver, page3_link)
        print("Pagination: Clicked on Page 3")
        time.sleep(2)
        
        # Select items from page 3
        page3_checkboxes = pagination_table.find_elements(By.XPATH, ".//tbody//input[@type='checkbox']")
        if page3_checkboxes and len(page3_checkboxes) >= 1:
            page3_checkboxes[0].click()
            print("Selected first item from page 3")

        # navigate to page 4
        page4_link = pagination_element.find_element(By.XPATH, ".//li/a[text()='4']")
        click(driver, page4_link)
        print("Pagination: Clicked on Page 4")
        time.sleep(2)

        # Select items from page 4
        page4_checkboxes = pagination_table.find_elements(By.XPATH, ".//tbody//input[@type='checkbox']")
        if page4_checkboxes and len(page4_checkboxes) >= 1:
            page4_checkboxes[0].click()
            print("Selected first item from page 4")

        # Go back to page 1
        page1_link = pagination_element.find_element(By.XPATH, ".//li/a[text()='1']")
        click(driver, page1_link)
        print("Pagination: Returned to Page 1")
        time.sleep(2)
    except Exception as e:
        print(f"Pagination test error: {e}")

    # --- Simple Labels And Links Test ---
    try:
        print("\n=== LABELS AND LINKS LIST ===")
        
        # Find and scroll to the Labels And Links section
        labels_section = driver.find_element(By.XPATH, "//h2[contains(text(), 'Labels And Links')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", labels_section)
        print("Scrolled to Labels And Links section")
        time.sleep(1)
        
        # Find the Labels and Links container
        links_container = driver.find_element(By.XPATH, "//h2[contains(text(), 'Labels And Links')]/following::div[1]")
        
        # Get all links in the section
        all_links = links_container.find_elements(By.TAG_NAME, "a")
        print(f"Found {len(all_links)} links in the Labels And Links section")
        
        # Print all links
        for i, link in enumerate(all_links):
            link_text = link.text.strip()
            link_href = link.get_attribute("href")
            print(f"{i+1}. {link_text}: {link_href}")
        
        print("Labels And Links listing completed")
        
    except Exception as e:
        print(f"Error listing Labels And Links: {e}")
        
    # --- Simple Form Filling ---
    try:
        print("\n=== FORM FILLING ===")
        
        # Find and scroll to Form section
        form_section = driver.find_element(By.XPATH, "//h2[text()='Form']")
        driver.execute_script("arguments[0].scrollIntoView(true);", form_section)
        print("Scrolled to Form section")
        time.sleep(1)
        
        # Fill and submit all three forms with simple approach
        input_fields = driver.find_elements(By.XPATH, "//input[@type='text' and contains(@class, 'input-field')]")
        submit_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Submit')]")
        
        # Fill each form in sequence
        for i in range(min(len(input_fields), len(submit_buttons))):
            # Fill the input field
            input_fields[i].clear()
            input_fields[i].send_keys(f"Test data {i+1}")
            print(f"Entered text in form {i+1}")
            
            # Click submit button
            submit_buttons[i].click()
            print(f"Clicked submit for form {i+1}")
            time.sleep(0.5)
        
        print("Form filling completed")
        
    except Exception as e:
        print(f"Error in form filling: {e}")

    # --- Footer Links Listing ---
    try:
        print("\n=== FOOTER LINKS LIST ===")
        
        # Find and scroll to the Footer Links section
        footer_section = driver.find_element(By.XPATH, "//h2[contains(text(), 'Footer Links')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", footer_section)
        print("Scrolled to Footer Links section")
        time.sleep(1)
        
        # Find all footer links
        footer_links = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Footer Links')]/following::li/a")
        print(f"Found {len(footer_links)} links in the Footer section")
        
        # Print all footer links
        for i, link in enumerate(footer_links):
            link_text = link.text.strip()
            link_href = link.get_attribute("href")
            print(f"{i+1}. {link_text}: {link_href}")
            
        print("Footer links listing completed")
        
    except Exception as e:
        print(f"Error listing Footer links: {e}")
    
    # --- Shadow DOM Content Listing ---
    try:
        print("\n=== SHADOW DOM CONTENT ===")
        
        
        
        # Find YouTube link with simple approach
        try:
            youtube_link = driver.find_element(By.XPATH, "//a[contains(@href, 'youtube')]")
            if youtube_link:
                print(f"\nYouTube Link: {youtube_link.get_attribute('href')}")
            else:
                print("\nNo YouTube link found")
        except:
            print("\nNo YouTube link found")
            
        print("Shadow DOM content listing completed")
        
    except Exception as e:
        print(f"Error listing shadow DOM content: {e}")

    print(f"Completed test for {name}")
    print("-" * 50)
# refresh the page for new entry from excel sheet
    driver.refresh()
    time.sleep(3)

# Close browser
driver.quit()

# Print completion message
print("\nAll tests completed successfully")
