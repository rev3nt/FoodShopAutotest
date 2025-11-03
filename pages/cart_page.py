from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    place_order_button_locator = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    cart_summ_locator = (By.XPATH, "//div[@class='mx-2 my-4 fs-5 text-end']")

    # Функция для получения суммы заказа в корзине
    def get_cart_summ(self):
        # Находим элемент на страницу, получаем текст
        result = self.find_element(self.cart_summ_locator).text
        # Вырезаем лишнее из строки, преобразуем в число для удобства
        result = int(result.replace('Итого: ', '')[:-2])

        return result

    # Функция, которая будет считать текущую сумму сделанных заказов(если корзина создана корректно и была пустой до теста)
    # Может стоит сделать что то более гибкое, только как? Можно собирать инфу с карточек, на надо ли это сравнить
    # наверное надо, потому что нужно убедиться в том, что корзина сформированна правильно.
    def checking_correct_cart_summ(self):


    # Оформить заказ
    def place_order(self):
        self.click_on(self.place_order_button_locator)