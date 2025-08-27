from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import openpyxl
import time

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

# Close browser
driver.quit()
print("\nAll tests completed successfully")
