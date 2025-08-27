from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import openpyxl
import time
from Framework.actions import click_element as click
from Framework.elementConstruct import construct_element

# ---------- Load Excel ----------
workbook = openpyxl.load_workbook("selenium-automation-practice/data.xlsx")
sheet = workbook.active

# ---------- Start Chrome ----------
service = Service("ChromeDriver.exe")
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
    name_field.clear()
    name_field.send_keys(name or "")
    print(f"Entered Name: {name}")
    time.sleep(THINKTIME)
    # --- Email ---
    email_field = driver.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys(email or "")
    print(f"Entered Email: {email}")
    time.sleep(THINKTIME)
    # --- Phone ---
    phone_field = driver.find_element(By.ID, "phone")
    phone_field.clear()
    phone_field.send_keys(str(phone or ""))
    print(f"Entered Phone: {phone}")
    time.sleep(THINKTIME)
    # --- Address / Comments ---
    address_field = driver.find_element(By.ID, "textarea")
    address_field.clear()
    address_field.send_keys(address or "")
    print(f"Entered Address: {address}")
    time.sleep(THINKTIME)
    # --- Gender ---
    if gender:
        gender_id = "male" if gender.lower().startswith("m") else "female"
        driver.find_element(By.ID, gender_id).click()
        print(f"Selected Gender: {gender}")
    print(f"days")
    # --- Days checkboxes ---
    if days:
        for day in days.split(","):
            day = day.strip()
            try:
                checkbox = driver.find_element(By.XPATH, f"//input[@name='day' and contains(@value,'{day}')]")
                checkbox.click()
                print(f"Checked Day: {day}")
            except:
                print(f"Checkbox for {day} not found")

    # --- Country dropdown ---
    if country:
        country_select = Select(driver.find_element(By.ID, "country"))
        country_select.select_by_visible_text(country)
        print(f"Selected Country: {country}")
    time.sleep(THINKTIME)
    # --- Colors dropdown ---
    if color:
        color_select = Select(driver.find_element(By.ID, "colors"))
        color_select.select_by_visible_text(color)
        print(f"Selected Color: {color}")
    time.sleep(THINKTIME)
    # --- Date picker ---
    if date1:
        date_str = date1.strftime("%m/%d/%Y") if hasattr(date1, 'strftime') else str(date1)
        driver.find_element(By.ID, "datepicker").clear()
        driver.find_element(By.ID, "datepicker").send_keys(date_str)
        print(f"Entered Date: {date_str}")
    time.sleep(THINKTIME)
    # --- File Upload ---
    if upload_file:
        driver.find_element(By.ID, "filename").send_keys(upload_file)
        print(f"Uploaded File: {upload_file}")
    time.sleep(THINKTIME)
    # --- Submit ---
    submit = construct_element(driver, By.XPATH, "//input[@value='Submit']")
    click(driver, submit)
    # driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    print("Clicked Submit button")
    time.sleep(3)
    time.sleep(THINKTIME)
    # --- Read Static Table ---
    print("\nStatic Table:")
    try:
        static_table = driver.find_element(By.XPATH, "//table[@border='1']")
        rows = static_table.find_elements(By.TAG_NAME, "tr")
        for r in rows[1:]:
            cols = r.find_elements(By.TAG_NAME, "td")
            data = [c.text for c in cols]
            print(data)
    except:
        print("Static table not found")
    time.sleep(THINKTIME)
    # --- Read Dynamic Table ---
    print("\nDynamic Table:")
    try:
        dynamic_table = driver.find_element(By.XPATH, "//table[@border='1' and .//th[text()='Name']]")
        rows = dynamic_table.find_elements(By.TAG_NAME, "tr")
        for r in rows[1:]:
            cols = r.find_elements(By.TAG_NAME, "td")
            data = [c.text for c in cols]
            print(data)
    except:
        print("Dynamic table not found")

# Close browser
driver.quit()
print("\nAll tests completed successfully")
