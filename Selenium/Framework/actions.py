

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

# Upload file with form submission
def upload_file_with_submit(driver, file_input_id, file_path, form_id=None, submit_button_xpath=None, status_id=None):
    """
    Enhanced file upload function that handles the complete file upload process including form submission.
    
    Args:
        driver: WebDriver instance
        file_input_id: ID of the file input element
        file_path: Path to the file to upload
        form_id: Optional - ID of the form to submit
        submit_button_xpath: Optional - XPath of the submit button
        status_id: Optional - ID of the element displaying upload status
    
    Returns:
        bool: True if upload was successful, False otherwise
    """
    try:
        # Find file input element
        file_input = driver.find_element(By.ID, file_input_id)
        file_input.send_keys(file_path)
        print(f"File selected: {file_path}")
        
        # Submit the form if needed
        if submit_button_xpath:
            try:
                submit_button = driver.find_element(By.XPATH, submit_button_xpath)
                submit_button.click()
                print("Submit button clicked")
            except Exception as e:
                print(f"Error clicking submit button: {e}")
                # Try form submission as fallback
                if form_id:
                    try:
                        form = driver.find_element(By.ID, form_id)
                        form.submit()
                        print(f"Form {form_id} submitted directly")
                    except Exception as form_error:
                        print(f"Error submitting form: {form_error}")
        
        # Check status if needed
        if status_id:
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, status_id))
                )
                status_element = driver.find_element(By.ID, status_id)
                print(f"Upload status: {status_element.text}")
            except Exception as status_error:
                print(f"Could not retrieve upload status: {status_error}")
        
        return True
    except Exception as e:
        print(f"Error during file upload process: {e}")
        return False

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
            cols = row.find_elements(By.TAG_NAME, "td") or row.find_elements(By.TAG_NAME, "th")
            data.append([col.text for col in cols])
        print("Table data extracted")
        return data
    except Exception as e:
        print(f"Error reading table: {e}")
        return []
        
# Get text from elements below a target element
def get_text_below_element(driver, target_element, selector_pattern=None):
    """
    Extracts text from elements that appear below a target element in the DOM.
    
    Args:
        driver: WebDriver instance
        target_element: The reference element to start searching from
        selector_pattern: Optional CSS or XPath selector to filter elements
        
    Returns:
        List of text strings from elements found below the target
    """
    try:
        # Get all text elements below the target using JavaScript
        if selector_pattern:
            # Use provided selector if available
            script = """
                var target = arguments[0];
                var results = [];
                var elements = document.querySelectorAll(arguments[1]);
                
                // Filter elements that are after the target in the DOM
                for (var i = 0; i < elements.length; i++) {
                    var element = elements[i];
                    if (target.compareDocumentPosition(element) & Node.DOCUMENT_POSITION_FOLLOWING) {
                        if (element.textContent && element.textContent.trim() !== '') {
                            results.push(element.textContent.trim());
                        }
                    }
                }
                return results;
            """
            return driver.execute_script(script, target_element, selector_pattern)
        else:
            # Default approach - get text from siblings that follow the target
            script = """
                var target = arguments[0];
                var results = [];
                var node = target;
                
                // Get text from following siblings
                while (node = node.nextSibling) {
                    if (node.nodeType === Node.ELEMENT_NODE && node.textContent && node.textContent.trim() !== '') {
                        results.push(node.textContent.trim());
                    }
                }
                
                // If no siblings with text, try parent's next siblings
                if (results.length === 0) {
                    node = target.parentNode;
                    while (node = node.nextSibling) {
                        if (node.nodeType === Node.ELEMENT_NODE && node.textContent && node.textContent.trim() !== '') {
                            results.push(node.textContent.trim());
                        }
                    }
                }
                
                return results;
            """
            return driver.execute_script(script, target_element)
    except Exception as e:
        print(f"Error getting text below element: {e}")
        return []

# Enhanced date picker interaction (click, enter value, close)
def interact_with_date_picker(driver, element, date_str):
    try:
        from selenium.webdriver.common.keys import Keys
        
        # Click to open calendar
        element.click()
        time.sleep(1)
        
        # Clear and enter date
        element.clear()
        element.send_keys(date_str)
        time.sleep(1)
        
        # Close the calendar by pressing Tab
        element.send_keys(Keys.TAB)
        time.sleep(1)
        
        # Alternative: click elsewhere to close it
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass
            
        print(f"Date picker interaction completed with date: {date_str}")
    except Exception as e:
        print(f"Error with date picker interaction: {e}")

# Set date range with two date inputs
# Parse a date range string into start and end dates
def parse_date_range(date_range_str):
    """
    Parse a date range string into start and end dates.
    Supports formats:
    - "MM/DD/YYYY-MM/DD/YYYY"
    - "MM/DD/YYYY to MM/DD/YYYY"
    - "MM/DD/YYYY - MM/DD/YYYY"
    - "Start: MM/DD/YYYY, End: MM/DD/YYYY"
    
    Args:
        date_range_str: String containing the date range
        
    Returns:
        Tuple of (start_date, end_date) strings in MM/DD/YYYY format
    """
    try:
        if not date_range_str or not isinstance(date_range_str, str):
            return None, None
            
        date_range_str = date_range_str.strip()
        
        # Try different separators
        for separator in ['-', 'to', ',']:
            if separator in date_range_str:
                parts = date_range_str.split(separator, 1)
                if len(parts) == 2:
                    # Clean up each part
                    start_raw = parts[0].strip()
                    end_raw = parts[1].strip()
                    
                    # Extract dates with regex pattern MM/DD/YYYY
                    import re
                    date_pattern = r'(\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4})'
                    
                    start_match = re.search(date_pattern, start_raw)
                    end_match = re.search(date_pattern, end_raw)
                    
                    if start_match and end_match:
                        start_date = start_match.group(1)
                        end_date = end_match.group(1)
                        
                        # Ensure MM/DD/YYYY format
                        if '-' in start_date:
                            month, day, year = start_date.split('-')
                            start_date = f"{month}/{day}/{year}"
                        if '-' in end_date:
                            month, day, year = end_date.split('-')
                            end_date = f"{month}/{day}/{year}"
                            
                        return start_date, end_date
        
        # If no separator patterns worked, try to find two dates
        import re
        date_matches = re.findall(r'(\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4})', date_range_str)
        if len(date_matches) >= 2:
            start_date = date_matches[0]
            end_date = date_matches[1]
            
            # Ensure MM/DD/YYYY format
            if '-' in start_date:
                month, day, year = start_date.split('-')
                start_date = f"{month}/{day}/{year}"
            if '-' in end_date:
                month, day, year = end_date.split('-')
                end_date = f"{month}/{day}/{year}"
                
            return start_date, end_date
    
        # If we couldn't extract two dates, return None
        return None, None
    except Exception as e:
        print(f"Error parsing date range: {e}")
        return None, None

def set_date_range(driver, start_field, end_field, start_date, end_date):
    try:
        # Check if we have a compound date range string
        if isinstance(start_date, str) and not end_date and ('-' in start_date or 'to' in start_date or ',' in start_date):
            parsed_start, parsed_end = parse_date_range(start_date)
            if parsed_start and parsed_end:
                start_date = parsed_start
                end_date = parsed_end
                print(f"Parsed date range: {start_date} to {end_date}")
        
        # Clear existing values
        start_field.clear()
        end_field.clear()
        
        # Use JavaScript for reliable input
        driver.execute_script("arguments[0].value = arguments[1];", start_field, start_date)
        driver.execute_script("arguments[0].value = arguments[1];", end_field, end_date)
        
        # Trigger change events
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", start_field)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", end_field)
        
        print(f"Date range set: {start_date} to {end_date}")
        return True
    except Exception as e:
        print(f"Error setting date range: {e}")
        return False

# Find element by multiple selectors
def find_element_by_multiple_selectors(driver, selectors, wait_time=5):
    element = None
    
    for selector in selectors:
        selector_type = selector[0]
        selector_value = selector[1]
        try:
            if wait_time > 0:
                element = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
            else:
                element = driver.find_element(selector_type, selector_value)
            if element:
                print(f"Found element using {selector_type}: {selector_value}")
                break
        except:
            continue
            
    return element

# Find element that contains text
def find_element_with_text(driver, text_to_find, tag_name="*"):
    try:
        xpath = f"//{tag_name}[contains(text(), '{text_to_find}')]"
        element = driver.find_element(By.XPATH, xpath)
        return element
    except Exception as e:
        print(f"Could not find element containing text '{text_to_find}': {e}")
        return None

# Select multiple items from a multi-select list
def select_from_multi_select(driver, element, options_to_select):
    try:
        from selenium.webdriver.support.ui import Select
        select_obj = Select(element)
        
        selected_options = []
        for option in options_to_select:
            try:
                select_obj.select_by_visible_text(option)
                selected_options.append(option)
                print(f"Selected option: {option}")
            except:
                print(f"Option '{option}' not found or could not be selected")
        
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
