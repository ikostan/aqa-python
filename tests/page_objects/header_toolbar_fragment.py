from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject


class HeaderToolbarFragment(BasePageObject):
    LOGIN_LINK = (By.CSS_SELECTOR, ".login-link")
    USER_AVATAR = (By.CSS_SELECTOR, ".aui-avatar-inner img")

    def __init__(self, driver):
        super().__init__(driver)

    def is_login_link_present(self):
        return self.is_element_present(self.LOGIN_LINK)

    def wait_until_login_link_is_present(self, timeout=10):
        return self.wait_until_element_is_present(self.driver, self.LOGIN_LINK, timeout)

    def is_user_avatar_present(self):
        return self.is_element_present(self.USER_AVATAR)

    def wait_until_user_avatar_is_present(self, timeout=10):
        return self.wait_until_element_is_present(self.driver, self.USER_AVATAR, timeout)
