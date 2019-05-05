from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject
from tests.page_objects.header_toolbar_fragment import HeaderToolbarFragment


class LoginPageObject(BasePageObject):
    PAGE_URL_PART = "/login.jsp?os_destination=%2Fdefault.jsp"
    LOGIN_INPUT = (By.ID, "login-form-username")
    PASSWORD_INPUT = (By.ID, "login-form-password")
    LOGIN_BUTTON = (By.ID, "login-form-submit")

    def __init__(self, driver):
        super().__init__(driver)
        self.header_toolbar = HeaderToolbarFragment(driver)

    def get_url(self):
        return self.get_base_url() + self.PAGE_URL_PART

    def open_page(self):
        page_url = self.get_url()
        self.driver.get(page_url)
        self.header_toolbar.wait_until_login_link_is_present()

    def input_login(self, login_for_input):
        self.driver.find_element(*self.LOGIN_INPUT).clear()
        self.driver.find_element(*self.LOGIN_INPUT).send_keys(login_for_input)

    def input_password(self, password_for_input):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password_for_input)

    def click_login_button(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def populate_inputs_and_submit(self, login_for_input, password_for_input):
        self.input_login(login_for_input)
        self.input_password(password_for_input)
        self.click_login_button()

    def login_user(self, login_for_input, password_for_input):
        self.open_page()
        self.populate_inputs_and_submit(login_for_input, password_for_input)
        return self.header_toolbar.wait_until_user_button_is_present()

    def enter_site_as_test_user(self):
        login_for_input = self.get_user_login()
        password_for_input = self.get_user_password()
        self.login_user(login_for_input, password_for_input)
