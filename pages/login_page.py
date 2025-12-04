from selenium.common import StaleElementReferenceException

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    # Локаторы элементов для взаимодействия
    username_locator = (By.XPATH, "//input[@type='text']")
    password_locator = (By.XPATH, "//input[@type='password']")
    login_button_locator = (By.XPATH, "//button[contains(text(), ' Войти ')]")
    shop_page_text_locator = (By.XPATH, "//a[contains(text(), 'Магазин')]")

    def __init__(self, url, driver):
        super().__init__(driver)
        self.url = url

    # Открываем страницу авторизации
    def open(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    # Вводим данные в поля и логинимся
    def login(self, username, password):
        # Вводим логин и пароль
        self.type_text(self.username_locator, username)
        print("Введен логин")
        self.type_text(self.password_locator, password)
        print("Введен пароль")

        try:
            # Нажимаем на кнопку логина
            self.click_on(self.login_button_locator)
            print("Кнопка логина нажата")
        except StaleElementReferenceException:
            print("Кнопка логина нажата(было вызвано исключение)")

    def assure_login(self):
        return self.is_visible(self.shop_page_text_locator, timeout=1)