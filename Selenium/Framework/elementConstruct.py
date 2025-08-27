
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#function to construct element from by and value
def construct_element(driver, by, value):
    try:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, value)))
        return element
    except Exception as e:
        print(f"Error constructing element {value}: {e}")
        return None
