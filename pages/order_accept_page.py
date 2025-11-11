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
        product_cards_locator = (By.XPATH,
                                 "//div[@class='store-container mx-auto']//div[contains(@class, 'store-card border overflow-hidden ms-2 my-1')]")

        return self.find_elements(product_cards_locator)

    # Функция для получения информации из карточки
    def get_product_info_from_card(self, product_card):
        # Проверяем видна ли карточка с товаром на экране, если нет, то пытаемся скролить до нее
        if not product_card.is_displayed():
            try:
                ActionChains(self.driver).scroll_to_element(product_card).perform()
            except Exception as e:
                print(f"Скролл до элемента не возможен: {e}")
                return None

        # Получаем информацию о продукте из карточки
        product_name = product_card.find_element(By.XPATH, ".//div[@class='card-title fs-6 text-success']").text

        product_info = product_card.find_element(By.XPATH, ".//div[@class='fs-7 align-content-center text-nowrap mb-1']").text.split(" шт. по ")

        product_amount = product_info[0]

        product_price = product_info[1]

        return product_name,product_amount, product_price

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

        # Распаковываем данные по переменным
        for product_name, product_amount, product_price in products_info:
            # Проверяем, есть ли данные
            if product_name is None:
                continue

            try:
                # Получаем референс от инпутов пользователя, на который будем ориентироваться
                expected_info = self.PRODUCT_INFO[product_name]
                # Если есть такой продукт, делаем проверку
                if expected_info:
                    # Проверяем количество и цену
                    assert int(product_amount) == expected_info['amount']

                    assert product_price == expected_info['price']

                    print(f'{product_name} успешно прошел проверку')
            # В случае ошибок возвращаем False
            except Exception as e:
                print(f"Ошибка проверки для продукта '{product_name}': {e}")

                return False

        return True

    def get_user_info(self):
        # Собираем всю необходимую для валидации страницы информацию и форматируем
        user_first_name = self.find_element(self.first_name_locator).text.replace('Имя: ', '')
        user_surname = self.find_element(self.surname_locator).text.replace('Фамилия: ', '')
        user_middle_name = self.find_element(self.middle_name_locator).text.replace('Отчество: ', '')
        user_address = self.find_element(self.address_locator).text.replace('Адрес доставки: ', '')
        user_card_name = self.find_element(self.card_locator).text.replace('Номер карты: ', '')

        # Возвращаем список, потом его необходимо будет изменять
        return [user_first_name, user_surname, user_middle_name, user_address, user_card_name]

    def get_expected_user_info(self):
        user_first_name = self.USER_INFO.get('name')
        user_surname = self.USER_INFO.get('surname')
        user_middle_name = self.USER_INFO.get('middle_name')
        user_address = self.USER_INFO.get('address')
        user_card_name = self.USER_INFO.get('card_number')

        return [user_first_name, user_surname, user_middle_name, user_address, user_card_name]

    def check_user_info(self):
        # Получаем информацию о пользователе со страницы
        user_info = self.get_user_info()

        expected_info = self.get_expected_user_info()

        if len(user_info) != len(expected_info):
            print("Информация для проверки неполная или некорректная")

            return False

        for item in  range(len(user_info)):
            try:
                # Проходимся по списку с информацией и ищем совпадения
                assert user_info[item] == expected_info[item]
            except Exception:
                print(f"Элемент {user_info[item]} не сходится с {expected_info[item]}")

                return False

        return True

    def check_product_summary(self, cart_amount, cart_summ):
        amount_locator = (By.XPATH, "//div[contains(text(), 'Количество товаров')]")
        summ_locator = (By.XPATH, "//div[contains(text(), 'Итоговая стоимость')]")

        try:
            # Получаем количество и сумму товаров на странице
            amount = int(self.find_element(amount_locator).text.replace('Количество товаров: ', ''))
            summ = int(self.find_element(summ_locator).text.replace('Итоговая стоимость: ', '').replace(' ₽', ''))

            # Проверяем соответствует ли это число изначальному количеству товара в корзине
            assert amount == cart_amount

            # Соответствует ли сумма в корзине сумме на странице подтверждения
            assert summ == cart_summ
            print("Проверка прошла успешно")

            return True

        except Exception as e:
            print(f"Ошибка при попытке сравнить данные в корзине и на странице подтверждения: {e}")

            return False

    # Завершить оформление заказа
    def checkout(self):
        self.click_on(self.checkout_button_locator)
