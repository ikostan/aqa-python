from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject


class HeaderToolbarFragment(BasePageObject):
    LOGIN_LINK = (By.CSS_SELECTOR, ".login-link")
    USER_BUTTON = (By.ID, "header-details-user-fullname")
    CREATE_BUTTON = (By.ID, "create_link")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_until_login_link_is_present(self, timeout=10):
        return self.wait_until_element_is_present(self.LOGIN_LINK, True, timeout)

    def wait_until_user_button_is_present(self, timeout=10):
        return self.wait_until_element_is_present(self.USER_BUTTON, True, timeout)

    def click_create_button(self):
        self.driver.find_element(*self.CREATE_BUTTON).click()
