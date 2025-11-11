import time

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class UserDataPage(BasePage):

    # Локаторы элементов страницы с вводом данных о пользователе
    name_locator = (By.XPATH, "//input[@placeholder='Имя']")
    surname_locator = (By.XPATH, "//input[@placeholder='Фамилия']")
    middle_name_locator = (By.XPATH, "//input[@placeholder='Отчество']")
    address_locator = (By.XPATH, "//input[@placeholder='Адрес доставки']")
    card_locator = (By.XPATH, "//input[@placeholder='Номер карты']")
    accept_button_locator = (By.XPATH, "//button[@type='submit']")

    # Заполняем форму данными
    def input_user_data(self):
        # Находим поля и помещаем в них данные
        self.type_text(self.name_locator, self.USER_INFO['name'])
        time.sleep(0.1)

        self.type_text(self.surname_locator, self.USER_INFO['surname'])
        time.sleep(0.1)

        self.type_text(self.middle_name_locator, self.USER_INFO['middle_name'])
        time.sleep(0.1)

        self.type_text(self.address_locator, self.USER_INFO['address'])
        time.sleep(0.1)

        self.type_text(self.card_locator, self.USER_INFO['card_number'])
        time.sleep(0.1)

    # Нажимаем на кнопку подтверждения заказа
    def click_place_order_button(self):
        self.click_on(self.accept_button_locator)