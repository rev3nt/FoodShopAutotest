import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pages.admin_page import AdminPage
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.order_accept_page import OrderAccept
from pages.shop_page import ShopPage
from pages.success_page import SuccessPage
from pages.user_data_page import UserDataPage


class TestCommonUser:
    # Класс для тестирования функциональности пользователя

    # URL-адреса страниц
    LOGIN_PAGE_URL = "http://91.197.96.80/"
    CART_PAGE_URL = "http://91.197.96.80/cart"
    CHECKOUT_PAGE_URL = "http://91.197.96.80/checkout"
    OVERVIEW_PAGE_URL = "http://91.197.96.80/checkoutOverview"

    # Учетные данные пользователя и администратора
    LOGIN = "покупатель2"
    PASSWORD = "покупатель2"
    ADMIN_LOGIN = "admin"
    ADMIN_PASSWORD = "admin"

    # Данные для создания товара
    CREATE_PRODUCT = {
        'name': 'Созданный товар',
        'description': 'Описания для созданного товара',
        'category': 'Категория для нового товара',
        'price': '52.52',
        'photo_url': 'https://avatars.mds.yandex.net/get-altay/13267750/'
                     '2a00000190643b653e4ca3be15b45d7cd80f/L_height'
    }

    # Данные для редактирования товара
    EDIT_PRODUCT = {
        'name': 'Новый товар',
        'description': 'Описание Новое',
        'category': 'Категория новая',
        'price': '42',
        'photo_url': 'пофик 2.0'
    }

    @staticmethod
    def get_chrome_driver():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option(
            "prefs", {"profile.password_manager_leak_detection": False}
        )
        options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)

        return driver

    @staticmethod
    def get_firefox_driver():
        profile = webdriver.FirefoxProfile()

        profile.set_preference("browser.sessionstore.resume_from_crash", False)
        profile.set_preference("browser.sessionstore.resume_session_once", True)
        profile.set_preference("signon.leakDetections.enable", False)

        options = webdriver.FirefoxOptions()
        options.profile = profile
        options.add_argument('--headless')

        driver = webdriver.Firefox(options=options)

        return driver

    @staticmethod
    def get_yandex_driver():
        options = webdriver.ChromeOptions()

        yandex_binary_path = (
            r"C:\Users\user\AppData\Local\Yandex\YandexBrowser\Application"
            r"\browser.exe"
        )
        options.binary_location = yandex_binary_path

        options.add_experimental_option("detach", True)
        options.add_experimental_option(
            "prefs", {"profile.password_manager_leak_detection": False}
        )
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-background-networking')
        options.add_argument('--headless')

        # Необходимо установить яндекс драйвер на гитхабе для проведения
        # тестов в Яндекс Браузере
        service_path = (
            r"C:\Program Files\yandexdriver-25.10.0.2474-win64"
            r"\yandexdriver.exe"
        )
        service = Service(service_path)

        driver = webdriver.Chrome(service=service, options=options)

        return driver

    @staticmethod
    def get_edge_driver():
        options = webdriver.EdgeOptions()

        options.add_experimental_option("detach", True)
        options.add_experimental_option(
            "prefs", {"profile.password_manager_leak_detection": False}
        )
        options.add_argument('--headless')

        driver = webdriver.Edge(options=options)

        return driver

    DRIVERS = {
        'chrome': get_chrome_driver,
        'firefox': get_firefox_driver,
        'yandex': get_yandex_driver,
        'edge': get_edge_driver
    }

    # Фикстура для инициализации драйвера и сброса данных о добавленных
    # продуктах
    @pytest.fixture(autouse=True)
    def setup(self):
        BasePage.PRODUCT_INFO = {}
        BasePage.USER_INFO = {}

        browser = 'chrome'

        self.driver = self.DRIVERS[browser]()

        yield
        self.driver.quit()

    def test_login_positive(self):
        # Позитивный тест авторизации с корректными данными
        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

    def test_login_negative(self):
        # Негативный тест авторизации с некорректными данными
        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login('123', '123')

        assert not login_page.assure_login()

    def test_login_empty(self):
        # Тест авторизации с пустыми полями ввода
        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login('', '')

        assert not login_page.assure_login()

    def test_add_item_to_cart(self):
        # Тест добавления товара в корзину
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page = ShopPage(self.driver)

        # Очищаем корзину, если в ней есть товары
        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        # Добавляем товар в корзину
        shop_page.add_product_to_cart_by_index(1)

        assert shop_page.get_cart_count() == 1

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Проверяем товары на соответствие добавленным
        cart_page.check_all_products_stats()

    def test_cart_save_between_sessions(self):
        # Тест сохранения товаров в корзине между сессиями
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page = ShopPage(self.driver)

        # Очищаем корзину, если в ней есть товары
        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        # Добавляем несколько товаров в корзину
        shop_page.add_product_to_cart_by_index(1, times=3)
        shop_page.add_product_to_cart_by_index(3, times=2)

        # Выходим из системы
        shop_page.logout()

        # Повторно логинимся
        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Проверяем товары на соответствие добавленным
        cart_page.check_all_products_stats()

    def test_positive_user_data_input(self):
        # Позитивный тест ввода пользовательских данных
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_data()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        # Если корзина пуста, добавляем товар
        if shop_page.get_cart_count() == 0:
            shop_page.add_product_to_cart_by_index(4, times=1)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.input_user_data()
        user_data_page.click_place_order_button()

        # Проверяем, что перешли на страницу подтверждения заказа
        assert self.driver.current_url == self.OVERVIEW_PAGE_URL

    def test_negative_user_data_input(self):
        # Негативный тест ввода пользовательских данных
        base_page = BasePage(self.driver)

        base_page.generate_negative_user_data()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        # Если корзина пуста, добавляем товар
        if shop_page.get_cart_count() == 0:
            shop_page.add_product_to_cart_by_index(4, times=1)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.input_user_data()
        user_data_page.click_place_order_button()

        # Проверяем, что остались на странице ввода данных
        # (некорректные данные)
        assert self.driver.current_url == self.CHECKOUT_PAGE_URL

    def test_skip_user_data_input(self):
        # Тест пропуска ввода пользовательских данных
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        # Если корзина пуста, добавляем товар
        if shop_page.get_cart_count() == 0:
            shop_page.add_product_to_cart_by_index(4, times=1)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        # Не заполняем форму, сразу нажимаем кнопку
        user_data_page.click_place_order_button()

        # Проверяем, что остались на странице ввода данных
        # (данные не заполнены)
        assert self.driver.current_url == self.CHECKOUT_PAGE_URL

    def test_data_validation_on_overview_page(self):
        # Тест валидации данных на странице подтверждения заказа
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_data()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        time.sleep(1)
        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        # Очищаем корзину, если в ней есть товары
        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        # Добавляем товары в корзину
        shop_page.add_product_to_cart_by_index(1)
        shop_page.add_product_to_cart_by_index(4, times=2)

        cart_amount = shop_page.get_cart_count()

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Проверяем товары на соответствие добавленным
        cart_page.check_all_products_stats()

        product_amount = base_page.get_product_amount()

        # Сохраняем сумму
        cart_summ = cart_page.get_cart_summ()

        assert cart_amount == product_amount

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.input_user_data()
        user_data_page.click_place_order_button()

        order_accept_page = OrderAccept(self.driver)

        # Проверяем данные на странице подтверждения заказа
        order_accept_page.check_all_products_stats()
        order_accept_page.check_product_summary(
            cart_amount=cart_amount, cart_summ=cart_summ
        )
        order_accept_page.check_user_info()

    def test_order_more_then_100_items(self):
        # Тест оформления заказа с более чем 100 товарами
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page = ShopPage(self.driver)

        # Очищаем корзину, если в ней есть товары
        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        # Добавляем 101 товар
        shop_page.add_product_to_cart_by_index(1, times=101)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        cart_page.place_order()

        # Проверяем, что остались на странице корзины (заказ не оформлен)
        assert self.driver.current_url == self.CART_PAGE_URL

    def test_order_more_then_100_k_summ(self):
        # Тест оформления заказа с суммой более 100 000
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        assert login_page.assure_login()

        shop_page = ShopPage(self.driver)

        # Добавляем товары до достижения суммы 100 000
        shop_page.add_product_to_cart_by_index(4, times=150)

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Увеличиваем количество товаров, пока сумма не достигнет 100 000
        while cart_page.get_cart_summ() < 100000:
            self.driver.back()
            shop_page.add_product_to_cart_by_index(4, times=10)
            shop_page.go_to_cart()

        cart_page.place_order()

        # Проверяем, что остались на странице корзины (заказ не оформлен)
        assert self.driver.current_url == self.CART_PAGE_URL

    def test_create_order(self):
        # Тест полного цикла создания заказа
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_data()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.LOGIN, self.PASSWORD)

        shop_page = ShopPage(self.driver)

        # Очищаем корзину, если в ней есть товары
        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        # Добавляем товары в корзину
        shop_page.add_product_to_cart_by_index(1)
        shop_page.add_product_to_cart_by_index(4, times=2)

        cart_amount = shop_page.get_cart_count()

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Проверяем товары на соответствие добавленным
        cart_page.check_all_products_stats()

        product_amount = base_page.get_product_amount()

        # Сохраняем сумму
        cart_summ = cart_page.get_cart_summ()

        assert cart_amount == product_amount

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.input_user_data()
        user_data_page.click_place_order_button()

        order_accept_page = OrderAccept(self.driver)

        # Проверяем данные на странице подтверждения заказа
        order_accept_page.check_user_info()
        order_accept_page.check_all_products_stats()
        order_accept_page.check_product_summary(
            cart_amount=cart_amount, cart_summ=cart_summ
        )

        # Завершаем оформление заказа
        order_accept_page.checkout()

        success_page = SuccessPage(self.driver)

        # Проверяем успешное создание заказа
        success_page.assure_success()
        success_page.back_to_shop()

    def test_add_item(self):
        # Тест добавления товара (администратор)
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.ADMIN_LOGIN, self.ADMIN_PASSWORD)

        admin_page = AdminPage(self.driver)

        admin_page.enter_admin_panel()
        admin_page.add_item(**self.CREATE_PRODUCT)

        assert admin_page.assure_item_presence_in_panel(
            self.CREATE_PRODUCT['name']
        )

    def test_edit_item(self):
        # Тест редактирования товара (администратор)
        base_page = BasePage(self.driver)

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.ADMIN_LOGIN, self.ADMIN_PASSWORD)

        admin_page = AdminPage(self.driver)

        admin_page.enter_admin_panel()
        admin_page.edit_item_by_name(
            self.CREATE_PRODUCT['name'], **self.EDIT_PRODUCT
        )

        assert admin_page.assure_item_presence_in_panel(
            self.EDIT_PRODUCT['name']
        )

    def test_delete_item(self):
        # Тест удаления товара (администратор)
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_data()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.ADMIN_LOGIN, self.ADMIN_PASSWORD)

        admin_page = AdminPage(self.driver)

        admin_page.enter_admin_panel()
        admin_page.delete_item_by_name(self.EDIT_PRODUCT['name'])

        time.sleep(0.2)

        assert not admin_page.assure_item_presence_in_panel(
            self.EDIT_PRODUCT['name']
        )

    def test_create_order_as_admin(self):
        # Тест создания заказа от имени администратора
        base_page = BasePage(self.driver)

        base_page.generate_positive_user_data()

        login_page = LoginPage(self.LOGIN_PAGE_URL, self.driver)

        login_page.open()
        login_page.login(self.ADMIN_LOGIN, self.ADMIN_PASSWORD)

        shop_page = ShopPage(self.driver)

        # Очищаем корзину, если в ней есть товары
        if shop_page.get_cart_count() != 0:
            shop_page.clear_cart()

        assert shop_page.get_cart_count() == 0

        # Добавляем товары в корзину
        shop_page.add_product_to_cart_by_index(1)
        shop_page.add_product_to_cart_by_index(4, times=2)

        cart_amount = shop_page.get_cart_count()

        shop_page.go_to_cart()

        cart_page = CartPage(self.driver)

        # Проверяем товары на соответствие добавленным
        cart_page.check_all_products_stats()

        product_amount = base_page.get_product_amount()

        # Сохраняем сумму
        cart_summ = cart_page.get_cart_summ()

        assert cart_amount == product_amount

        # Переходим на страницу заполнения пользовательских данных
        cart_page.place_order()

        user_data_page = UserDataPage(self.driver)

        user_data_page.input_user_data()
        user_data_page.click_place_order_button()

        order_accept_page = OrderAccept(self.driver)

        # Проверяем данные на странице подтверждения заказа
        order_accept_page.check_user_info()
        order_accept_page.check_all_products_stats()
        order_accept_page.check_product_summary(
            cart_amount=cart_amount, cart_summ=cart_summ
        )

        # Завершаем оформление заказа
        order_accept_page.checkout()

        success_page = SuccessPage(self.driver)

        # Проверяем успешное создание заказа
        success_page.assure_success()
        success_page.back_to_shop()