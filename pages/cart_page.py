from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    place_order_button_locator = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    cart_summ_locator = (By.XPATH, "//div[@class='mx-2 my-4 fs-5 text-end']")
    cards_container_locator = (By.XPATH, "//div[@class='store-card-container d-grid m-2']")

    # Функция для получения суммы заказа в корзине
    def get_cart_summ(self):
        # Находим элемент на страницу, получаем текст
        result = self.find_element(self.cart_summ_locator).text
        # Вырезаем лишнее из строки, преобразуем в число для удобства

        result = float(result.replace('Итого: ', '')[:-2])
        return result

    # Функция для получения контейнера с карточками
    def get_all_product_cards(self):
        product_cards_locator = (By.XPATH, "//div[@class='store-card-container d-grid m-2']//div[contains(@class, 'store-card border rounded-1 overflow-hidden my-1')]")

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
        product_name = product_card.find_element(By.XPATH, ".//div[@class='card-title fs-4 text-success']").text
        product_price = product_card.find_element(By.XPATH,
                                                 ".//div[@class='fs-5 align-content-center m-1 text-nowrap']").text
        amount_input = product_card.find_element(By.XPATH,
                                                 ".//input[contains(@class, 'form-control')]")

        product_amount = amount_input.get_attribute('value')

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

    # Оформить заказ
    def place_order(self):
        self.click_on(self.place_order_button_locator)