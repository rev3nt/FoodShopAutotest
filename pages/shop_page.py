from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pages.base_page import BasePage


class ShopPage(BasePage):
    cart_locator = (By.XPATH, "//span[contains(text(), 'shopping_cart')]")
    select_locator = (By.XPATH, "//select[@aria-label='Выбор по умолчанию']")

    # Добавить товар в корзину по заготовленному заранее локатору
    def add_product_to_cart_by_index(self, index, times=1):
        product_card_locator = (By.XPATH, f"//div[@class='store-card-container d-grid m-2']/div[{index}]")

        try:
            product_card = self.find_element(product_card_locator)
        except NoSuchElementException:
            print("Элемент с таким индексом не был найден на странице")
            return


        product_add_button = product_card.find_element(By.XPATH, ".//button[.//span[contains(text(), 'add')]]")

        if not self.is_visible(product_add_button):
            try:
                ActionChains(self.driver).scroll_to_element(product_card).perform()
            except:
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
    def add_product_by_category_to_cart(self, category, times=1):
        product_card_locator = (By.XPATH, f"//div[@cat='{category}']//button[.//span[contains(text(), 'add')]")



        try:
            product_card = self.find_element(product_card_locator)
        except NoSuchElementException:
            print("Элемент с введенной категорией не найден")
            return

        product_add_button = product_card.find_element(By.XPATH, ".//button[.//span[contains(text(), 'add')]")

        if not self.is_visible(product_card):
            try:
                ActionChains(self.driver).scroll_to_element(product_card).perform()
            except:
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

    # Фильтрация товара
    def filter_by_value(self, value):
        select = Select(self.find_element(self.select_locator))

        try:
            # Выставляем необходимое значение
            select.select_by_value(value)
        except NoSuchElementException:
            print('Индекс за границами диапазона select')