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
        self.type_text(self.name_locator, self.USER_INFO[0])

        self.type_text(self.surname_locator, self.USER_INFO[0]['surname'])

        self.type_text(self.middle_name_locator, self.USER_INFO[0]['middle_name'])

        self.type_text(self.address_locator, self.USER_INFO[0]['address'])

        self.type_text(self.card_locator, self.USER_INFO[0]['card_number'])

    # Нажимаем на кнопку подтверждения заказа
    def click_place_order_button(self):
        self.click_on(self.accept_button_locator)