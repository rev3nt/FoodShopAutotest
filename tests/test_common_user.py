import time
import pytest
from selenium import webdriver

from pages.admin_page import AdminPage
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
    ADMIN_LOGIN = "admin"
    ADMIN_PASSWORD = "admin"

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

    def test_login_positive(self):
        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

    def test_login_negative(self):
        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login('123', '123')

        assert login_page.assure_login() == False

    def test_login_empty(self):
        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login('', '')

        assert login_page.assure_login() == False

    def test_add_item_to_cart(self):
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page = ShopPage(self.driver)

        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()
            print('Почистил корзину')

        assert shop_page.get_cart_count() == 0
        print("Все кул")

        shop_page.add_product_to_cart_by_index(1)
        print("Добавил товар")

        assert shop_page.get_cart_count() == 1
        print("Все кул")

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Проверяем товары на соответствие добавленным
        assert cart_page.check_all_products_stats()

    def test_cart_save_between_sessions(self):
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page = ShopPage(self.driver)

        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        shop_page.add_product_to_cart_by_index(1, times=3)

        shop_page.add_product_to_cart_by_index(3, times=2)

        shop_page.logout()

        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Проверяем товары на соответствие добавленным
        assert cart_page.check_all_products_stats()

    def test_order_more_then_100_items(self):
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page = ShopPage(self.driver)

        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        shop_page.add_product_to_cart_by_index(1, times=101)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        cart_page.place_order()

        assert self.driver.current_url == 'http://91.197.96.80/cart'

    def test_order_more_then_100_k_summ(self):
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page = ShopPage(self.driver)

        shop_page.add_product_to_cart_by_index(4, times=150)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        while cart_page.get_cart_summ() < 100000:
            self.driver.back()

            shop_page.add_product_to_cart_by_index(4, times=10)

            shop_page.go_to_cart()

        cart_page.place_order()

        assert self.driver.current_url == 'http://91.197.96.80/cart'

    def test_positive_user_data_input(self):
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_date()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        time.sleep(1)

        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        if shop_page.get_cart_count() == 0:
            shop_page.add_product_to_cart_by_index(4, times=1)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.input_user_data()

        user_data_page.click_place_order_button()

        assert self.driver.current_url == 'http://91.197.96.80/checkoutOverview'

    def test_negative_user_data_input(self):
        base_page = BasePage(self.driver)

        base_page.generate_negative_user_date()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        time.sleep(1)

        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        if shop_page.get_cart_count() == 0:
            shop_page.add_product_to_cart_by_index(4, times=1)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.input_user_data()

        user_data_page.click_place_order_button()

        assert self.driver.current_url == 'http://91.197.96.80/checkout'

    def test_skip_user_data_input(self):
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        time.sleep(1)

        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        if shop_page.get_cart_count() == 0:
            shop_page.add_product_to_cart_by_index(4, times=1)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.click_place_order_button()

        assert self.driver.current_url == 'http://91.197.96.80/checkout'

    def test_data_validation_on_overview_page(self):
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

        assert order_accept_page.check_all_products_stats()

        assert order_accept_page.check_product_summary(cart_amount=cart_amount, cart_summ=cart_summ)

        assert order_accept_page.check_user_info()

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

        assert order_accept_page.check_user_info()

        assert order_accept_page.check_all_products_stats()

        assert order_accept_page.check_product_summary(cart_amount=cart_amount, cart_summ=cart_summ)

        order_accept_page.checkout()

        time.sleep(1)

        success_page = SuccessPage(self.driver)

        success_page.assure_success()

        success_page.back_to_shop()

    def test_add_item(self):
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        time.sleep(1)

        login_page.login(self.ADMIN_LOGIN, self.ADMIN_PASSWORD)

        admin_page = AdminPage(self.driver)

        admin_page.enter_admin_panel()

        admin_page.add_item()

        time.sleep(2)

    def test_edit_item(self):
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        time.sleep(1)

        login_page.login(self.ADMIN_LOGIN, self.ADMIN_PASSWORD)

        admin_page = AdminPage(self.driver)

        admin_page.enter_admin_panel()

        admin_page.edit_item_by_id(10)

        time.sleep(2)

    def test_delete_item(self):
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_date()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        time.sleep(1)

        login_page.login(self.ADMIN_LOGIN, self.ADMIN_PASSWORD)

        admin_page = AdminPage(self.driver)

        admin_page.enter_admin_panel()

        time.sleep(1)

        admin_page.delete_item_by_id(10)
        time.sleep(2)

    def test_create_order_as_admin(self):
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_date()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()

        time.sleep(1)

        login_page.login(self.ADMIN_LOGIN, self.ADMIN_PASSWORD)

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

        assert order_accept_page.check_user_info()

        assert order_accept_page.check_all_products_stats()

        assert order_accept_page.check_product_summary(cart_amount=cart_amount, cart_summ=cart_summ)

        order_accept_page.checkout()

        time.sleep(1)

        success_page = SuccessPage(self.driver)

        success_page.assure_success()

        success_page.back_to_shop()