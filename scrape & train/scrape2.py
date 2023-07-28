import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
import csv

driver = webdriver.Chrome()

driver.get(
    "https://ec.europa.eu/growth/tools-databases/cosing/reference/functions/list/pH ADJUSTERS"
)
driver.implicitly_wait(30)
table_data = []

while True:
    function = driver.find_element(
        By.XPATH, "/html/body/app-root/ecl-app/main/div/ng-component/h6/strong[3]"
    ).text.lower()
    ingredients = driver.find_elements(
        By.XPATH,
        "/html/body/app-root/ecl-app/main/div/ng-component/app-results-subs/table/tbody/tr/td[2]/a",
    )
    for i in ingredients:
        table_data.append([i.text.strip().lower(), "ph adjusters"])
        print(i.text)

    try:
        next_button = driver.find_element(
            By.XPATH, '//a[@aria-label="Go to next page"]'
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        next_button.click()
        time.sleep(10)
    except NoSuchElementException:
        break

driver.quit()
print(table_data)

with open("ingredient-function.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(table_data)
