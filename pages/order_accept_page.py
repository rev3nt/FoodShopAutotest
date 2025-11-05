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

    # Функция для получения контейнера с карточками
    def get_all_product_cards(self):
        product_cards_locator = (By.XPATH, "//div[contains(@class, 'store-card')]")

        return self.find_elements(product_cards_locator)

    # Функция для получения информации из карточки
    def get_product_info_from_card(self, product_card):
        # Проверяем видна ли карточка с товаром на экране, если нет, то пытаемся скролить до нее
        if not self.is_visible(product_card):
            try:
                ActionChains(self.driver).scroll_to_element(product_card).perform()
            except Exception as e:
                print(f"Скролл до элемента не возможен: {e}")
                return None

        # Получаем информацию о продукте из карточки
        product_name = product_card.find_element(By.XPATH, ".//div[@class='card-title fs-6 text-success'").text
        product_info = product_card.find_element(By.XPATH, ".//div[@class='fs-7 align-content-center text-nowrap mb-1']").text

        # Строка вида X шт. по Y ₽
        parts = product_info.split(' шт. по ')

        # Разбиваем строку на нужные переменные
        product_amount = parts[0]
        product_price = parts[1]

        return product_name, product_amount, product_price

    # Функция для получения информации из карточек
    def get_all_products_stats(self):
        product_cards = self.get_all_product_cards()
        products_info = []

        for card in product_cards:
            try:
                product_info = self.get_product_info_from_card(card)
                if product_info:
                    products_info.append(product_info)

                    print(f'Карточка: {product_info}')
                else:
                    print("Не удалось получить информацию из карточки")
            except Exception as e:
                print(e)

        return products_info

    # Проверяем все продукты из карточек на совпадение с информацией со словаря
    def check_all_products_stats(self):
        products_info = self.get_all_products_stats()

        for product_name, product_amount, product_price in products_info:
            if product_name is None:
                continue

            try:
                expected_info = self.PRODUCT_INFO[product_name]
                if expected_info:
                    assert product_amount == expected_info['amount']

                    assert product_price == expected_info['price']

                    print(f'{product_name} успешно прошел проверку')
            except AssertionError as e:
                print(f"Ошибка проверки для продукта '{product_name}': {e}")

    def get_user_info(self):
        # Собираем всю необходимую для валидации страницы информацию и форматируем
        user_first_name = self.find_element(self.first_name_locator).text.replace('Имя: ', '')
        user_surname = self.find_element(self.surname_locator).text.replace('Фамилия: ', '')
        user_middle_name = self.find_element(self.middle_name_locator).text.replace('Отчество: ', '')
        user_address = self.find_element(self.address_locator).text.replace('Адрес доставки: ', '')
        user_card_name = self.find_element(self.card_locator).text.replace('Номер карты: ', '')
        user_amount = self.find_element(self.amount_locator).text.replace('Количество товаров: ', '')
        user_price = self.find_element(self.price_locator).text.replace('Итоговая стоимость: ', '')

        # Возвращаем список, потом его необходимо будет изменять
        return [user_first_name, user_surname, user_middle_name, user_address, user_card_name, user_amount, user_price]

    def check_user_info(self):
        # Получаем информацию о пользователе со страницы
        user_info = self.get_user_info()

        # Сохраняем имя, по нему будет обращение в словарь со сгенерированными данными пользователя
        user_first_name = user_info[0]
        # Удаляем этот элемент, чтобы пробегаться по списку и проверять остальную информацию
        user_info.pop(0)

        try:
            # Проходимся по списку с информацией и ищем совпадения
            for item in user_info:
                assert item in self.PRODUCT_INFO[user_first_name]
        except KeyError:
            print("Элемент не сходится с информацией, представленной в форме пользователя")

    # Завершить оформление заказа
    def checkout(self):
        self.click_on(self.checkout_button_locator)
