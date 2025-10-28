from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OrderAccept(BasePage):
    checkout_button_locator = (By.XPATH, "//button[contains(text(), ' Завершить заказ ')]")

    first_name_locator = (By.XPATH, "//div[@class='fs-6 ms-3'][1]//div[1]")
    surname_locator = (By.XPATH, "//div[@class='fs-6 ms-3'][1]//div[2]")
    middle_name_locator = (By.XPATH, "//div[@class='fs-6 ms-3'][1]//div[3]")

    address_locator = (By.XPATH, "//div[@class='fs-6 ms-3'][2]//div[1]")

    card_locator = (By.XPATH, "//div[@class='fs-6 ms-3'][3]//div[2]")

    amount_locator = (By.XPATH, "//div[@class='fs-6 ms-3'][4]//div[1]")
    price_locator = (By.XPATH, "//div[@class='fs-6 ms-3'][4]//div[2]")

    def get_product_info_by_id(self, index):
        # Формируем локатор на карточку с нужным индексом
        product_card_locator = (By.XPATH, f"//div[@class='store-container']//div[contains(@class, 'store-card')][{index}]")

        # Ищем карточку по локатору
        try:
            product_card = self.find_element(product_card_locator)
        except NoSuchElementException:
            print("Элемент с данным индексом не был найден")
            return None

        # Проверяем видна ли карточка с товаром на экране, если нет, то пытаемся скролить до нее
        if not self.is_visible(product_card):
            try:
                ActionChains(self.driver).scroll_to_element(product_card).perform()
            except:
                print("Скролл до элемента не возможен")
                return None

        # Получаем информацию о продукте из карточки
        product_name = product_card.find_element(By.XPATH, "//div[@class='card-title fs-6 text-success'").text
        product_info = product_card.find_element(By.XPATH, "//div[@class='fs-7 align-content-center text-nowrap mb-1']").text

        # Строка вида X шт. по Y ₽
        parts = product_info.split(' шт. по ')

        # Разбиваем строку на нужные переменные
        product_amount = parts[0]
        product_price = parts[1]

        return product_name, product_amount, product_price

    # Проверка продукта по словарю
    def check_product_stats(self):
        product_name, product_amount, product_price = self.get_product_info_by_id(0)

        if product_name is None:
            return

        try:
            assert product_amount in self.PRODUCT_INFO[product_name]

            assert product_price in self.PRODUCT_INFO[product_amount]
        except KeyError:
            print("Продукта с таким названием не было в корзине")

    def get_user_info(self):
        # Собираем всю необходимую для валидации страницы и форматируем под необходимый формат
        user_first_name = self.find_element(self.first_name_locator).text.replace('Имя: ', '')
        user_surname = self.find_element(self.surname_locator).text.replace('Фамилия: ', '')
        user_middle_name = self.find_element(self.middle_name_locator).text.replace('Отчество: ', '')
        user_address = self.find_element(self.address_locator).text.replace('Адрес доставки: ', '')
        user_card_name = self.find_element(self.card_locator).text.replace('Номер карты: ', '')
        user_amount = self.find_element(self.amount_locator).text.replace('Количество товаров: ', '')
        user_price = self.find_element(self.price_locator).text.replace('Итоговая стоимость: ', '')

        return user_first_name, user_surname, user_middle_name, user_address, user_card_name, user_amount, user_price

    def check_user_info(self):
        user_info = self.get_user_info()

        user_first_name = user_info[0]
        user_surname = user_info[1]
        user_middle_name = user_info[2]
        user_address = user_info[3]
        user_card_name = user_info[4]
        user_amount = user_info[5]
        user_price = user_info[6]

        try:
            assert user_surname in self.PRODUCT_INFO[user_first_name]

            assert user_middle_name in self.PRODUCT_INFO[user_first_name]

            assert user_address in self.PRODUCT_INFO[user_address]

            assert user_card_name in self.PRODUCT_INFO[user_address]

            assert user_amount in self.PRODUCT_INFO[user_amount]

            assert user_price in self.PRODUCT_INFO[user_amount]
        except KeyError:
            print("Элемент не сходится с информацией, представленной в форме пользователя")

    # Завершить оформление заказа
    def checkout(self):
        self.click_on(self.checkout_button_locator)
