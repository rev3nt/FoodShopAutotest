import time
from tabnanny import check

import pytest

from selenium import webdriver
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.order_accept_page import OrderAccept
from pages.shop_page import ShopPage
from pages.success_page import SuccessPage
from pages.user_data_page import UserDataPage


class TestCommonUser:
    LOGIN_PAGE_URL = "http://91.197.96.80/"
    LOGIN = "покупатель2"
    PASSWORD = "покупатель2"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome(options=self.get_options())
        yield
        self.driver.quit()

    @staticmethod
    def get_options():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option("prefs", {"profile.password_manager_leak_detection": False})

        return options

    def test_login(self):
        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login(), "Пользователь не перешел на страницу магазина"

        time.sleep(3)

    def test_create_order(self):
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_date()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        time.sleep(1)

        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        shop_page.add_product_to_cart_by_index(1)

        shop_page.add_product_to_cart_by_index(4, times=2)

        cart_amount = shop_page.get_cart_count()

        shop_page.go_to_cart()

        time.sleep(1)

        cart_page = CartPage(self.driver)

        # Проверяем товары на соответствие добавленным
        assert cart_page.check_all_products_stats()

        product_amount = base_page.get_product_amount()
        product_summ = base_page.get_product_summ()

        # Сохраняем сумму
        cart_summ = cart_page.get_cart_summ()

        assert cart_amount == product_amount

        assert cart_summ == cart_summ

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.input_user_data()

        user_data_page.click_place_order_button()

        time.sleep(1)

        order_accept_page = OrderAccept(self.driver)

        # assert order_accept_page.check_user_info()

        assert order_accept_page.check_all_products_stats()

        assert order_accept_page.check_product_summary(cart_amount=cart_amount, cart_summ=cart_summ)

        order_accept_page.checkout()

        time.sleep(1)

        success_page = SuccessPage(self.driver)

        success_page.assure_success()

        success_page.back_to_shop()

        print("Тест завершен")