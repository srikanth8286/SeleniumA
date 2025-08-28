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
    get_table_data
)
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
    if days:
        for day in days.split(","):
            day = day.strip()
            try:
                checkbox = driver.find_element(By.XPATH, f"//input[@name='day' and contains(@value,'{day}')]")
                select_radio(checkbox)
                print(f"Checked Day: {day}")
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
    # --- Date picker ---
    if date1:
        date_str = date1.strftime("%m/%d/%Y") if hasattr(date1, 'strftime') else str(date1)
        date_field = driver.find_element(By.ID, "datepicker")
        pick_date(date_field, date_str)
    time.sleep(THINKTIME)
    # --- File Upload ---
    if upload_file:
        file_input = driver.find_element(By.ID, "filename")
        upload_file(file_input, upload_file)
    time.sleep(THINKTIME)
    # --- Submit ---
    submit = construct_element(driver, By.XPATH, "//input[@value='Submit']")
    click(driver, submit)
    print("Clicked Submit button")
    time.sleep(3)
    time.sleep(THINKTIME)
    # --- Read Static Table ---
    print("\nStatic Table:")
    try:
        static_table = driver.find_element(By.XPATH, "//table[@border='1']")
        static_data = get_table_data(static_table)
        for row in static_data[1:]:
            print(row)
    except:
        print("Static table not found")
    time.sleep(THINKTIME)
    # --- Read Dynamic Table ---
    print("\nDynamic Table:")
    try:
        dynamic_table = driver.find_element(By.XPATH, "//table[@border='1' and .//th[text()='Name']]")
        dynamic_data = get_table_data(dynamic_table)
        for row in dynamic_data[1:]:
            print(row)
    except:
        print("Dynamic table not found")

# Close browser
driver.quit()
print("\nAll tests completed successfully")
