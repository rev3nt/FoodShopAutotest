from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class SuccessPage(BasePage):
    success_text_locator = (By.XPATH, "//div[@class='navbar-brand']")
    back_to_shop_button_locator = (By.XPATH, "//button[contains(text(), ' Вернуться в магазин ')]")

    success_text = "Оформление заказа: Заказ успешно создан"
    success_url = "http://91.197.96.80/checkoutComplete"

    def assure_success(self):
        current_url = self.driver.current_url
        text = self.find_element(self.success_text_locator).text

        assert text == self.success_text

        assert current_url == self.success_url

        print("Заказ был успешно создан")

    def back_to_shop(self):
        self.click_on(self.back_to_shop_button_locator)