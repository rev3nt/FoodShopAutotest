import time

import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class AdminPage(BasePage):
    edit_name_locator = (By.XPATH, '//input[@placeholder="Наименование"]')
    edit_description_locator = (By.XPATH, '//input[@placeholder="Описание"]')
    edit_category_locator = (By.XPATH, '//input[@placeholder="Ожидаемая Категория"]')
    edit_price_locator = (By.XPATH, '//input[@placeholder="Цена"]')
    edit_url_locator = (By.XPATH, '//input[@placeholder="Image Source"]')

    update_item_locator = (By.XPATH, '//button[contains(text(), " Обновить товар ")]')
    add_item_locator = (By.XPATH, '//button[contains(text(), "Добавить товар")]')
    create_item_button_locator = (By.XPATH, '//button[contains(text(), "Создать товар")]')

    add_category_locator = (By.XPATH, '//input[@placeholder="Ожидаемая категория"]')

    # Вход в админ панель из окна магазина
    def enter_admin_panel(self):
        # Локатор кнопки меню и входа в админ панель
        menu_button_locator = (By.XPATH, '//button[@class="btn btn-light btn-sm d-flex"]')
        admin_panel_button_locator = (By.XPATH, '//a[@class="nav-link"]')

        # Переходим в админ панель
        self.click_on(menu_button_locator)
        time.sleep(0.5)

        self.click_on(admin_panel_button_locator)

        print('Вход в админ панель успешно выполнен')

    def delete_item_by_id(self, item_id):
        card_locator = (By.XPATH,
                        f"//div[@class='store-container mx-auto']/div[{item_id}]")

        try:
            product_card = self.find_element(card_locator)
        except NoSuchElementException:
            pytest.fail("Элемент с таким индексом не был найден на странице")
            return

        product_delete_button = product_card.find_element(By.XPATH, ".//button//span[contains(text(), 'delete')]")

        try:
            if not product_delete_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(product_card).perform()

        except Exception:
            pytest.fail("Не удалось проскролить до элемента")

            return

        try:
            self.click_on(product_delete_button)

            print(f'Объект под номером {item_id} был удален')

        except Exception:
            pytest.fail("Не удалось нажать на кнопку удаления товара")

    def delete_item_by_name(self, item_name):
        card_locator = (By.XPATH, f'//div[contains(text(), "{item_name}")]/ancestor::div[@role="button"]')

        try:
            product_card = self.find_element(card_locator)
        except NoSuchElementException:
            pytest.fail('Карточка с таким названием не была найдена')

            return

        product_delete_button = product_card.find_element(By.XPATH, ".//button//span[contains(text(), 'delete')]")

        try:
            if not product_delete_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(product_card).perform()

        except Exception:
            pytest.fail('Не удалось проскролить до кнопки удаления')

        try:
            self.click_on(product_delete_button)

            print(f'Объект под названием {item_name} был удален')

        except Exception:
            pytest.fail("Не удалось нажать на кнопку удаления товара")

    def edit_item_by_id(self, item_id):
        card_locator = (By.XPATH,
                        f"//div[@class='store-container mx-auto']/div[{item_id}]")

        try:
            product_card = self.find_element(card_locator)

        except NoSuchElementException:
            pytest.fail("Элемент с таким индексом не был найден на странице")
            return

        product_edit_button = product_card.find_element(By.XPATH, ".//button//span[contains(text(), 'edit')]")

        try:
            if not product_edit_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(product_card).perform()

        except Exception:
            pytest.fail("Не удалось проскролить до элемента")

            return

        try:
            self.click_on(product_edit_button)

        except Exception:
            pytest.fail("Не удалось нажать на кнопку редактирования товара")

        time.sleep(1)

        try:
            self.type_text(self.edit_name_locator, 'Название')

            self.type_text(self.edit_description_locator, 'Описание')

            self.type_text(self.edit_category_locator, 'Категория')

            self.type_text(self.edit_price_locator, '220.56')

            self.type_text(self.edit_url_locator, 'пофик')

        except Exception:
            pytest.fail('Не удалось вписать данные в поля')

        update_button = self.find_element(self.update_item_locator)

        try:
            if not update_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(product_card).perform()

        except Exception:
            pytest.fail('Не удалось проскролить до кнопки подтверждения редактирования')

        try:
            self.click_on(self.update_item_locator)

            print(f'Объект под номером {item_id} был изменен')

        except Exception:
            pytest.fail("Не удалось нажать на кнопку подтверждения изменения товара")

    def edit_item_by_name(self, item_name):
        card_locator = (By.XPATH, f'//div[contains(text(), "{item_name}")]/ancestor::div[@role="button"]')

        try:
            product_card = self.find_element(card_locator)
        except NoSuchElementException:
            pytest.fail("Элемент с таким индексом не был найден на странице")
            return

        product_edit_button = product_card.find_element(By.XPATH, ".//button//span[contains(text(), 'edit')]")

        try:
            if not product_edit_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(product_card).perform()

        except Exception:
            pytest.fail("Не удалось проскролить до элемента")

            return

        try:
            self.click_on(product_edit_button)

        except Exception:
            pytest.fail("Не удалось нажать на кнопку редактирования товара")

        time.sleep(1)

        try:
            self.type_text(self.edit_name_locator, 'Название Новое')

            self.type_text(self.edit_description_locator, 'Описание Новое')

            self.type_text(self.edit_category_locator, 'Категория новая')

            self.type_text(self.edit_price_locator, '42')

            self.type_text(self.edit_url_locator, 'пофик 2.0')

        except Exception:
            pytest.fail('Не удалось вписать данные в поля')

        update_button = self.find_element(self.update_item_locator)

        try:
            if not update_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(product_card).perform()

        except Exception:
            pytest.fail('Не удалось проскролить до кнопки подтверждения редактирования')

        try:
            self.click_on(self.update_item_locator)

            print(f'Товар под названием {item_name} был успешно изменен')

        except Exception:
            pytest.fail("Не удалось нажать на кнопку подтверждения изменения товара")

    def add_item(self):
        add_button = self.find_element(self.add_item_locator)

        try:
            if not add_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(add_button).perform()

        except Exception:
            pytest.fail('Не удалось проскролить до кнопки добавления товара')

        try:
            self.click_on(self.add_item_locator)

        except Exception:
            pytest.fail('Не удалось нажать на кнопку добавления')

        try:
            self.type_text(self.edit_name_locator, 'Созданный товар')

            self.type_text(self.edit_description_locator, 'Описания для созданного товара')

            self.type_text(self.add_category_locator, 'Категория для нового товара')

            self.type_text(self.edit_price_locator, '52.52')

            self.type_text(self.edit_url_locator, 'https://avatars.mds.yandex.net/get-altay/13267750/2a00000190643b653e4ca3be15b45d7cd80f/L_height')

        except Exception:
            pytest.fail('Не удалось вписать данные в поля')

        create_button = self.find_element(self.create_item_button_locator)

        try:
            if not create_button.is_displayed():
                ActionChains(self.driver).scroll_to_element(create_button).perform()

        except Exception:
            pytest.fail("Не удалось проскролить до кнопки подтверждения создания товара")

        try:
            self.click_on(self.create_item_button_locator)

        except Exception:
            pytest.fail('Не удалось нажать на кнопку подтверждения создания товара')

    def back_to_shop(self):
        shop_button_locator = (By.XPATH, '//a[@class="navbar-brand"]')

        try:
            self.click_on(shop_button_locator)

        except Exception:
            pytest.fail("Не удалось нажать на кнопку возвращения в магазин")