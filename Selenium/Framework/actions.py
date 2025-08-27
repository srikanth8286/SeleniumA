from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#click function
def click_element(driver, element):
    try:
        element.click()
        print("Clicked element")
    except Exception as e:
        print(f"Error clicking element: {e}")
