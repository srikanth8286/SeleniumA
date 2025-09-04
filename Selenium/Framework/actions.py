from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import datetime
import time

# Click an element
def click_element(driver, element):
    try:
        element.click()
        print(f"Clicked element: {element}")
        return True
    except Exception as e:
        print(f"Error clicking element: {e}")
        return False

# Input text into element
def input_text(element, text):
    try:
        element.clear()
        element.send_keys(text)
        print(f"Entered text: {text}")
        return True
    except Exception as e:
        print(f"Error entering text: {e}")
        return False

# Select radio button
def select_radio(element):
    try:
        element.click()
        print(f"Selected radio: {element}")
        return True
    except Exception as e:
        print(f"Error selecting radio: {e}")
        return False

# Select dropdown option by visible text
def select_dropdown_by_text(element, text):
    try:
        select = Select(element)
        select.select_by_visible_text(text)
        print(f"Selected dropdown option: {text}")
        return True
    except Exception as e:
        print(f"Error selecting dropdown: {e}")
        return False

# Upload file via input element
def upload_file(element, file_path):
    try:
        element.send_keys(file_path)
        print(f"File uploaded: {file_path}")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

# Enhanced file upload with form submission and status check
def upload_file_with_submit(driver, file_input_id, file_path, form_id=None, submit_button_xpath=None, status_id=None):
    try:
        # Find file input and upload file
        try:
            file_input = driver.find_element(By.ID, file_input_id)
            file_input.send_keys(file_path)
            print(f"File selected: {file_path}")
        except Exception as input_error:
            print(f"Error finding file input or uploading file: {input_error}")
            
            # Try alternative approach with xpath
            try:
                file_input = driver.find_element(By.XPATH, f"//input[@id='{file_input_id}']")
                file_input.send_keys(file_path)
                print(f"File selected using xpath: {file_path}")
            except Exception as xpath_error:
                print(f"Error with xpath approach: {xpath_error}")
                return False
        
        # Submit the form if form_id is provided
        if form_id:
            try:
                form = driver.find_element(By.ID, form_id)
                form.submit()
                print("Form submitted by form.submit()")
            except Exception as form_error:
                print(f"Error submitting form: {form_error}")
                return False
        
        # Click submit button if provided
        elif submit_button_xpath:
            try:
                submit_button = driver.find_element(By.XPATH, submit_button_xpath)
                submit_button.click()
                print(f"Submit button clicked: {submit_button_xpath}")
            except Exception as button_error:
                print(f"Error clicking submit button: {button_error}")
                return False
        
        # Check upload status if status_id is provided
        if status_id:
            try:
                # Wait for status to appear
                wait = WebDriverWait(driver, 10)
                status_element = wait.until(EC.presence_of_element_located((By.ID, status_id)))
                print(f"Upload status: {status_element.text}")
            except Exception as status_error:
                print(f"Could not retrieve upload status: {status_error}")
        
        return True
    except Exception as e:
        print(f"Error during file upload process: {e}")
        return False

# Scroll to an element
def scroll_to_element(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print("Scrolled to element")
        return True
    except Exception as e:
        print(f"Error scrolling to element: {e}")
        return False

# Validate element text
def validate_text(element, expected_text):
    try:
        actual_text = element.text
        is_valid = actual_text == expected_text
        print(f"Text validation: {'Passed' if is_valid else 'Failed'}, Expected: '{expected_text}', Actual: '{actual_text}'")
        return is_valid
    except Exception as e:
        print(f"Error validating text: {e}")
        return False

# Take screenshot
def take_screenshot(driver, file_path):
    try:
        driver.save_screenshot(file_path)
        print(f"Screenshot saved: {file_path}")
        return True
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return False

# Select date in date picker
def pick_date(element, date_str):
    try:
        element.clear()
        element.send_keys(date_str)
        print(f"Date selected: {date_str}")
        return True
    except Exception as e:
        print(f"Error picking date: {e}")
        return False

# Extract data from an HTML table
def get_table_data(table_element):
    try:
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        table_data = []
        for row in rows:
            row_data = []
            cells = row.find_elements(By.TAG_NAME, "td")
            if not cells:  # Try th for header row
                cells = row.find_elements(By.TAG_NAME, "th")
            for cell in cells:
                row_data.append(cell.text)
            if row_data:  # Only add non-empty rows
                table_data.append(row_data)
        print(f"Table data extracted: {len(table_data)} rows")
        return table_data
    except Exception as e:
        print(f"Error extracting table data: {e}")
        return []

# Get text content below a specific element
def get_text_below_element(driver, target_element, selector_pattern=None):
    try:
        # Get all text nodes after the target element
        text_script = """
            function getTextNodesAfter(element) {
                let result = [];
                let found = false;
                
                function traverse(node) {
                    if (node === element) {
                        found = true;
                        return;
                    }
                    
                    if (found && node.nodeType === 3 && node.textContent.trim()) {
                        // Text node with non-empty content
                        result.push(node.textContent.trim());
                    } else if (node.nodeType === 1) {
                        // Element node
                        if (found && (
                            node.tagName === 'P' || 
                            node.tagName === 'DIV' || 
                            node.tagName === 'SPAN' ||
                            node.tagName === 'LI'
                        )) {
                            if (node.textContent.trim()) {
                                result.push(node.textContent.trim());
                            }
                        }
                        
                        // Check children
                        for (let i = 0; i < node.childNodes.length; i++) {
                            traverse(node.childNodes[i]);
                        }
                    }
                }
                
                traverse(document.body);
                return result;
            }
            return getTextNodesAfter(arguments[0]);
        """
        text_items = driver.execute_script(text_script, target_element)
        
        # Filter by pattern if provided
        if selector_pattern and text_items:
            pattern = re.compile(selector_pattern)
            filtered_items = [item for item in text_items if pattern.search(item)]
            print(f"Found {len(filtered_items)} text items matching pattern")
            return filtered_items
        
        print(f"Found {len(text_items)} text items below element")
        return text_items
    except Exception as e:
        print(f"Error getting text below element: {e}")
        return []

# Function to interact with date picker
def interact_with_date_picker(driver, element, date_str):
    try:
        # First try simple approach
        element.clear()
        element.send_keys(date_str)
        print(f"Date entered: {date_str}")
        
        # Handle calendar if it appears
        try:
            # Look for calendar day element
            date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y")
            day = str(date_obj.day)
            
            # Wait for a short time to see if calendar appears
            time.sleep(0.5)
            
            # Try to find and click the day
            calendar_days = driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-calendar td a")
            for cal_day in calendar_days:
                if cal_day.text == day:
                    cal_day.click()
                    print(f"Clicked day {day} in calendar")
                    break
        except Exception as calendar_error:
            # Calendar may not have appeared, which is fine
            pass
            
        return True
    except Exception as e:
        print(f"Error interacting with date picker: {e}")
        return False

# Set date range with start and end dates
def set_date_range(driver, start_field, end_field, start_date, end_date):
    try:
        # Set start date
        success_start = interact_with_date_picker(driver, start_field, start_date)
        
        # Set end date
        success_end = interact_with_date_picker(driver, end_field, end_date)
        
        if success_start and success_end:
            print(f"Date range set: {start_date} to {end_date}")
            
            # Take screenshot to verify
            screenshot_path = "date_range_test.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
            return True
        else:
            print("Failed to set complete date range")
            return False
            
    except Exception as e:
        print(f"Error setting date range: {e}")
        return False

# Function to find elements using multiple different selectors
def find_element_by_multiple_selectors(driver, selectors, wait_time=5):
    """
    Try to find an element using multiple selector strategies.
    
    Args:
        driver: WebDriver instance
        selectors: Dictionary with keys as selector type (id, xpath, css, etc.) and values as selector strings
        wait_time: Time to wait for element
        
    Returns:
        First element found or None if not found
    """
    for selector_type, selector_value in selectors.items():
        try:
            wait = WebDriverWait(driver, wait_time)
            if selector_type.lower() == 'id':
                element = wait.until(EC.presence_of_element_located((By.ID, selector_value)))
            elif selector_type.lower() == 'xpath':
                element = wait.until(EC.presence_of_element_located((By.XPATH, selector_value)))
            elif selector_type.lower() == 'css':
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_value)))
            elif selector_type.lower() == 'name':
                element = wait.until(EC.presence_of_element_located((By.NAME, selector_value)))
            else:
                continue
                
            print(f"Element found using {selector_type}: {selector_value}")
            return element
        except Exception:
            continue
    
    print(f"Element not found using any of the provided selectors")
    return None

# Find an element containing specific text
def find_element_with_text(driver, text_to_find, tag_name="*"):
    try:
        xpath = f"//{tag_name}[contains(text(), '{text_to_find}')]"
        element = driver.find_element(By.XPATH, xpath)
        print(f"Found element with text: {text_to_find}")
        return element
    except Exception as e:
        print(f"Error finding element with text '{text_to_find}': {e}")
        return None

# Select options from multi-select element
def select_from_multi_select(driver, element, options_to_select):
    try:
        # Ensure element is a select element
        if element.tag_name.lower() != "select":
            print("Element is not a select element")
            return []
        
        # Create Select object
        select = Select(element)
        
        # Check if it's a multi-select
        if not select.is_multiple:
            print("This is not a multi-select element")
            return []
        
        # Clear existing selections
        select.deselect_all()
        
        # Track successfully selected options
        selected_options = []
        
        # Select requested options
        for option_text in options_to_select:
            try:
                select.select_by_visible_text(option_text)
                selected_options.append(option_text)
                print(f"Selected option: {option_text}")
            except Exception as option_error:
                print(f"Could not select option '{option_text}': {option_error}")
        
        # Return actually selected items
        return selected_options
    except Exception as e:
        print(f"Error in multi-select: {e}")
        return []

# Check/uncheck checkbox based on day name
def select_day_checkbox(driver, day):
    try:
        day = day.strip()
        xpath = f"//input[@id='{day.lower()}' and contains(@value,'{day.lower()}')]"
        checkbox = driver.find_element(By.XPATH, xpath)
        checkbox.click()
        is_selected = checkbox.is_selected()
        print(f"Day checkbox '{day}' clicked, selected status: {is_selected}")
        return is_selected
    except Exception as e:
        print(f"Checkbox for '{day}' not found or could not be clicked: {e}")
        return False

# Parse date range from text (since this is referenced in Sample.py but missing)
def parse_date_range(text):
    try:
        # Expected format: "Start Date: mm/dd/yyyy, End Date: mm/dd/yyyy"
        pattern = r"Start Date: (\d{2}/\d{2}/\d{4}),\s*End Date: (\d{2}/\d{2}/\d{4})"
        match = re.search(pattern, text)
        
        if match:
            start_date = match.group(1)
            end_date = match.group(2)
            print(f"Parsed date range: {start_date} to {end_date}")
            return start_date, end_date
        else:
            print("Could not parse date range, using defaults")
            return "01/01/2023", "12/31/2023"  # Default fallback
    except Exception as e:
        print(f"Error parsing date range: {e}")
        return "01/01/2023", "12/31/2023"  # Default fallback
