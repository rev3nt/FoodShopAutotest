from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("prefs", {"profile.password_manager_leak_detection": False})

driver = webdriver.Chrome(options=options)
driver.get("http://91.197.96.80/")

driver.maximize_window()

driver.find_element(By.XPATH, "//input[@type='text']").send_keys('покупатель4')
driver.find_element(By.XPATH, "//input[@type='password']").send_keys('покупатель4')

driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

selector_locator = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@aria-label='Выбор по умолчанию']")))

select = Select(selector_locator)

select.select_by_index(2)

time.sleep(3)

driver.quit()