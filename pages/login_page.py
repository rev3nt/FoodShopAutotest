from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    # Локаторы элементов для взаимодействия
    username_locator = (By.XPATH, "//input[@type='text']")
    password_locator = (By.XPATH, "//input[@type='password']")
    login_button_locator = (By.XPATH, "//button[contains(text(), 'Войти')]")

    def __init__(self, url, driver):
        super().__init__(driver)
        self.url = url


    # Открываем страницу авторизации
    def open(self):
        self.driver.get(self.url)

    # Вводим данные в поля и логинимся
    def login(self, username, password):
        # Вводим логин и пароль
        self.type_text(username, self.username_locator)
        print("Введен логин")
        self.type_text(password, self.password_locator)
        print("Введен пароль")

        # Нажимаем на кнопку логина
        self.click_on(self.login_button_locator)
