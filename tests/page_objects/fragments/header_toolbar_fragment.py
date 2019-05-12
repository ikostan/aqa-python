from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.page_objects.base_page_object import BasePageObject


class HeaderToolbarFragment(BasePageObject):
    LOGIN_LINK = (By.CSS_SELECTOR, ".login-link")
    USER_BUTTON = (By.ID, "header-details-user-fullname")
    CREATE_BUTTON = (By.ID, "create_link")
    SEARCH_INPUT = (By.ID, "quickSearchInput")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_until_login_link_is_present(self, timeout=10):
        return self.wait_until_element_is_present(self.LOGIN_LINK, True, timeout)

    def wait_until_user_button_is_present(self, timeout=10):
        return self.wait_until_element_is_present(self.USER_BUTTON, True, timeout)

    def click_create_button(self):
        self.driver.find_element(*self.CREATE_BUTTON).click()

    def populate_search_and_submit(self, search_string):
        input_field = self.driver.find_element(*self.SEARCH_INPUT)
        input_field.click()
        input_field.clear()
        input_field.send_keys(search_string)
        input_field.send_keys(Keys.ENTER)
