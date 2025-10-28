from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

class BasePage:
    PRODUCT_NAME = ""
    PRODUCT_AMOUNT = 0
    PRODUCT_PRICE = ""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # Поиск элемента на странице
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    # Клик на элемент, с ожидаем кликабельности, для удобства добавлена возможность нажимать несколько раз
    def click_on(self, locator, times=1):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        for _ in range(times):
            element.click()

    # Ввод текста по локатору
    def type_text(self, locator, text):
        element = self.wait.until(EC.element_to_be_clickable(locator))

        element.clear()

        element.send_keys(text)

    # Функция, которая проверяет, находится ли элемент на видимом экране
    def is_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return False