import time
import pytest

from selenium import webdriver
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.shop_page import ShopPage


class TestCommonUser:
    LOGIN_PAGE_URL = "http://91.197.96.80/"
    LOGIN = "покупатель3"
    PASSWORD = "покупатель3"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome(options=self.get_options())
        # yield
        # self.driver.quit()

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
        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        shop_page.add_product_to_cart_by_index(1)

        shop_page.add_product_to_cart_by_index(4, times=2)

        # shop_page.add_product_to_cart_by_category("БЕРГЕР", times=2)

        #assert shop_page.cart_and_user_input_comparison(), "Товар был добавлен некорректно"

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)
        print(cart_page.get_cart_summ())

        time.sleep(3)