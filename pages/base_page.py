import time

from faker import Faker
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

class BasePage:
    # Данные о выбранном товаре
    PRODUCT_INFO = {}

    # Данный о пользователе
    USER_INFO = {}

    def __init__(self, driver=None):
        self.driver = driver

    # Функция для генерации пользовательских данных
    def generate_positive_user_date(self):
        faker = Faker("ru_RU")

        self.USER_INFO.update({
            'name': faker.first_name(),
            'surname': faker.last_name(),
            'middle_name': faker.first_name(),
            'address': "ул. Тестовая, д. 1, кв. 1",
            'card_number': faker.credit_card_number()
        })

    # Поиск элемента на странице
    def find_element(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))

    # Возвращаем список элементов
    def find_elements(self, locator, delay=10):
        return WebDriverWait(self.driver, delay).until(EC.presence_of_all_elements_located(locator))

    # Клик на элемент, с ожидаем кликабельности, для удобства добавлена возможность нажимать несколько раз
    def click_on(self, locator, times=1):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        for _ in range(times):
            element.click()
            time.sleep(0.2)

    # Ввод текста по локатору
    def type_text(self, locator, text):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))

        element.clear()

        element.send_keys(text)

    # Функция, которая проверяет, находится ли элемент на видимом экране
    def is_visible(self, locator):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))

            return True
        except TimeoutException:
            print("Элемент не найден на странице")

            return False

    def get_product_amount(self):
        result = 0

        for product_name, product_data in self.PRODUCT_INFO.items():
            result += product_data['amount']

        print(f'Количество товаров, добавленных пользователем: {result}')

        return result

    def get_product_summ(self):
        result = 0

        for product_name, product_data in self.PRODUCT_INFO.items():
            result += float(product_data['price'].replace('₽', '').strip()) * product_data['amount']

        print(f'Сумма товаров, добавленных пользователем: {result}')

        return result