from tests.credentials import credentials
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


class BasePageObject:
    DEF_TIMEOUT = 4
    BASE_URL = "https://jira.hillel.it"
    USER_LOGIN = credentials.user_login
    USER_PASSWORD = credentials.user_password
    PROJECT_KEY = credentials.project_key
    PROJECT_NAME_FULL = credentials.project_name_full
    PROJECT_NAME_SHORT = credentials.project_name_short

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(self.DEF_TIMEOUT)

    def get_base_url(self):
        return self.BASE_URL

    def get_user_login(self):
        return self.USER_LOGIN

    def get_user_password(self):
        return self.USER_PASSWORD

    def get_project_key(self):
        return self.PROJECT_KEY

    def get_project_name_full(self):
        return self.PROJECT_NAME_FULL

    def get_project_name_short(self):
        return self.PROJECT_NAME_SHORT

    def get_current_url(self):
        return self.driver.current_url

    # element states
    def is_element_present(self, element):
        return EC.presence_of_element_located(element)

    def is_element_clickable(self, element):
        return EC.element_to_be_clickable(element)

    def is_string_contains_substring(self, string, sub_string):
        if sub_string in string:
            return True
        else:
            return False

    # element attributes
    def get_element_attribute(self, locator, attribute):
        return self.driver.find_element(*locator).get_attribute(attribute)

    # element waits
    def wait_until_element_is_present(self, element, timeout=5):
        self.driver.implicitly_wait(0)
        try:
            got_element = WebDriverWait(self.driver, timeout).until(self.is_element_present(element))
            result = got_element.is_displayed()
        except:
            result = False
        finally:
            method_result = result
        self.driver.implicitly_wait(self.DEF_TIMEOUT)
        return method_result

    def wait_until_element_is_not_present(self, element, timeout=5):
        self.driver.implicitly_wait(0)
        try:
            got_element = WebDriverWait(self.driver, timeout).until_not(self.is_element_present(element))
            result = got_element.is_displayed()
        except:
            result = False
        finally:
            method_result = result
        self.driver.implicitly_wait(self.DEF_TIMEOUT)
        return method_result

    def wait_until_element_is_clickable(self, element, timeout=5):
        self.driver.implicitly_wait(0)
        try:
            got_element = WebDriverWait(self.driver, timeout).until(self.is_element_clickable(element))
            result = got_element.is_displayed()
        except:
            result = False
        finally:
            method_result = result
        self.driver.implicitly_wait(self.DEF_TIMEOUT)
        return method_result

    def wait_until_element_is_not_clickable(self, element, timeout=5):
        self.driver.implicitly_wait(0)
        try:
            got_element = WebDriverWait(self.driver, timeout).until_not(self.is_element_clickable(element))
            result = got_element.is_displayed()
        except:
            result = False
        finally:
            method_result = result
        self.driver.implicitly_wait(self.DEF_TIMEOUT)
        return method_result

    def wait_until_attribute_value_is(self, locator, attribute, value, timeout=2):
        WebDriverWait(self.driver, timeout).until(self.get_element_attribute(locator, attribute) == value)

    # element actions
    def pick_in_combobox(self, combobox_locator, item_value):
        combobox_element = self.driver.find_element(*combobox_locator)
        combobox_element_input = combobox_element.find_element_by_css_selector("input")
        combobox_element.click()
        combobox_element_input.clear()
        combobox_element_input.send_keys(item_value)
        combobox_element_input.send_keys(Keys.TAB)

    # other methods
    def slice_off_substring(self, string, sliced_substring):
        full_string_len = len(string)
        sliced_substring_len = len(sliced_substring)
        return string[sliced_substring_len:full_string_len]
