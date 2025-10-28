from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from faker import Faker

class BasePage:
    # Данные о выбранном товаре
    PRODUCT_INFO = {}

    # Данный о пользователе
    USER_INFO = {}

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # Функция для генерации пользовательских данных
    def generate_positive_user_date(self):
        faker = Faker("en_US")

        self.USER_INFO[faker.first_name()] = {
            'surname': faker.last_name(),
            'middle_name': faker.first_name(),
            'address': faker.address(),
            'card_number': faker.card_number()
        }

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
            self.wait.until(EC.visibility_of_element_located(locator))

            return True
        except TimeoutException:
            print("Элемент не найден на странице")

            return False