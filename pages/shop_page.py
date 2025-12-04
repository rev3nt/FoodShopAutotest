import time

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage


class ShopPage(BasePage):
    cart_locator = (By.XPATH, "//span[contains(text(), 'shopping_cart')]")
    select_locator = (By.XPATH, "//select[@aria-label='Выбор по умолчанию']")
    cart_amount_locator = (By.XPATH, "//span[contains(@class, 'cart-counter')]")
    menu_locator = (By.XPATH, "//span[contains(text(), 'menu')]")
    logout_locator = (By.XPATH, "//div[contains(text(), 'Выход')]")

    def __init__(self, driver):
        super().__init__(driver)
        time.sleep(1)
        self.initial_cart_count = self.get_cart_count()

    # Добавить товар в корзину по заготовленному заранее локатору
    def add_product_to_cart_by_index(self, index, times=1):
        product_card_locator = (By.XPATH, f"//div[@class='store-card-container d-grid m-2']/div[{index}]")

        try:
            product_card = self.find_element(product_card_locator)
        except NoSuchElementException:
            print("Элемент с таким индексом не был найден на странице")
            return


        product_add_button = product_card.find_element(By.XPATH, ".//button[.//span[contains(text(), 'add')]]")

        try:
            if not product_add_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(product_card).perform()
        except Exception:
            print("Не удалось проскролить до элемента")
            return

        # Формируем данные для будущей верификации, данные достаем из карточки товара
        product_name = product_card.find_element(By.XPATH, ".//div[@class='card-title fs-4 text-success']").text
        product_price = product_card.find_element(By.XPATH, ".//div[@class='fs-5 align-content-center m-3']").text
        product_amount = times

        self.PRODUCT_INFO[product_name] = {
            'price': product_price,
            'amount': product_amount
        }

        # Нажимаем на кнопку добавления товара
        self.click_on(product_add_button, times=times)
        print(f"Товар добавлен {times} раз")

    # Добавить товар из определенной категории
    def add_product_to_cart_by_category(self, category, times=1):
        product_card_locator = (By.XPATH, f"//div[@cat='{category}']")

        try:
            product_card = self.find_element(product_card_locator)
        except NoSuchElementException:
            print("Элемент с введенной категорией не найден")
            return

        product_add_button = product_card.find_element(By.XPATH, ".//button[.//span[contains(text(), 'add')]]")

        try:
            if not product_add_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(product_card).perform()
        except Exception:
            print("Не удалось проскролить до элемента")
            return

        # Сохраняем данные о продукте
        product_name = product_card.find_element(By.XPATH, ".//div[@class='card-title fs-4 text-success']").text
        product_price = product_card.find_element(By.XPATH, ".//div[@class='fs-5 align-content-center m-3']").text
        product_amount = times

        self.PRODUCT_INFO[product_name] = {
            'price': product_price,
            'amount': product_amount
        }

        self.click_on(product_add_button, times=times)

        print(f"Элемент с категорий {category} добавлен {times} раз в корзину")

    # Переход в корзину
    def go_to_cart(self):
        self.click_on(self.cart_locator)
        print("Переадресация в корзину")

    def get_cart_count(self):
        return int(self.find_element(self.cart_amount_locator).text)

    # Считаем количество добавленных продуктов и извлекаем значение из корзины и сравниванием
    def cart_and_user_input_comparison(self):
        sum_of_user_inputs = 0

        # Считаем все инпуты пользователя
        for product in self.PRODUCT_INFO.items():
            sum_of_user_inputs += product[1]['amount']

        time.sleep(0.5)

        cart_amount = int(self.find_element(self.cart_amount_locator).text)

        result_amount = cart_amount - self.initial_cart_count

        print(f"Количество добавленных пользователем продуктов: {sum_of_user_inputs}")
        print(f"Количество товаров в корзине: {result_amount}")

        return  sum_of_user_inputs == result_amount

    # Фильтрация товара
    def filter_by_value(self, value):
        select = Select(self.find_element(self.select_locator))

        try:
            # Выставляем необходимое значение
            select.select_by_value(value)
        except NoSuchElementException:
            print('Индекс за границами диапазона select')

    # Функция для отчистки корзины
    def clear_cart(self):
        try:
            # Переходим в корзину
            self.click_on(self.cart_locator)
            time.sleep(1)

            # Локатор для кнопок удаления
            remove_button_locator = (By.XPATH,
                                     "//button[@class='btn btn-light btn-sm d-flex']//span[contains(text(), 'remove')]")

            # Получаем все кнопки удаления
            remove_buttons = self.find_elements(remove_button_locator)

            print(f"Найдено товаров для удаления: {len(remove_buttons)}")

            # Удаляем все товары по одному
            while remove_buttons:
                try:
                    # Кликаем на первую кнопку удаления
                    remove_buttons[0].click()
                    time.sleep(0.1)

                    # Обновляем список кнопок
                    remove_buttons = self.find_elements(remove_button_locator, delay=0.2)
                    print(f"Осталось товаров: {len(remove_buttons)}")

                except Exception:
                    break

            print("Корзина очищена")

            # Возвращаемся назад
            self.driver.back()

        except Exception as e:
            print(f"Ошибка при очистке корзины: {e}")

    # Функция для выхода из аккаунта пользователя
    def logout(self):
        self.click_on(self.menu_locator)

        self.click_on(self.logout_locator)

        print("Выход из аккаунта прошел успешно")