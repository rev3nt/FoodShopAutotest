from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pages.base_page import BasePage


class ShopPage(BasePage):
    first_product_add_locator = (By.XPATH, "//div[@cat='Гвозди']//button[.//span[contains(text(), 'add')]]")
    cart_locator = (By.XPATH, "//span[contains(text(), 'shopping_cart')]")
    select_locator = (By.XPATH, "//select[@aria-label='Выбор по умолчанию']")

    # Добавить товар в корзину по заготовленному заранее локатору
    def add_product_to_cart_by_index(self, index, times=1):
        try:
            product_card =self.find_element((By.XPATH, f"//div[@class='store-card-container d-grid m-2']/div[{index}]"))

            # Формируем данные для будущей верификации сформированных отчетов
            self.PRODUCT_NAME = product_card.find_element(By.XPATH, ".//div[@class='card-title fs-4 text-success']").text
            self.PRODUCT_PRICE = product_card.find_element(By.XPATH, ".//div[@class='fs-5 align-content-center m-3']").text
            self.PRODUCT_AMOUNT = times

            product_add_button = product_card.find_element(By.XPATH, ".//button[.//span[contains(text(), 'add')]]")

            product_add_button.click(times)


        except NoSuchElementException:
            print("Элемент с таким индексом не был найден на странице")

        self.click_on(self.first_product_add_locator, times=times)
        print(f"Товар добавлен {times} раз")

    # Добавить товар из определенной категории
    def add_product_by_category_to_cart(self, category, times=1):
        product_locator = (By.XPATH, f"//div[@cat='{category}']//button[.//span[contains(text(), 'add')]")

        try:
            if self.is_visible(product_locator):
                self.click_on(product_locator, times=times)

            print(f"Элемент с категорий {category} добавлен {times} раз в корзину")
        except NoSuchElementException:
            print("Элемент с введенной категорией не найден")

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