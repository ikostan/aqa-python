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
    def is_element_displayed(self, element, timeout=0):
        self.driver.implicitly_wait(timeout)
        try:
            self.driver.find_element(*element)
            result = True
        except:
            result = False
        finally:
            method_result = result
        self.driver.implicitly_wait(self.DEF_TIMEOUT)
        return method_result

    def is_string_contains_substring(self, string, sub_string):
        if sub_string in string:
            return True
        else:
            return False

    # element attributes
    def get_element_attribute(self, locator, attribute):
        return self.driver.find_element(*locator).get_attribute(attribute)

    # element waits
    def do_wait(self, expected_condition, true_or_false_for_until_or_not, timeout=5):
        self.driver.implicitly_wait(0)
        try:
            result = None
            if true_or_false_for_until_or_not:
                WebDriverWait(self.driver, timeout).until(expected_condition)
                result = True
            elif not true_or_false_for_until_or_not:
                WebDriverWait(self.driver, timeout).until_not(expected_condition)
                result = True
        except:
            result = False
        finally:
            method_result = result
        self.driver.implicitly_wait(self.DEF_TIMEOUT)
        return method_result

    def wait_until_element_is_present(self, element, true_or_false_for_present_or_not, timeout=5):
        return self.do_wait(EC.presence_of_element_located(element), true_or_false_for_present_or_not, timeout)

    def wait_until_element_is_clickable(self, element, true_or_false_for_clickable_or_not, timeout=5):
        return self.do_wait(EC.element_to_be_clickable(element), true_or_false_for_clickable_or_not, timeout)

    def wait_until_element_is_visible(self, locator, true_or_false_for_visible_or_not, timeout=2):
        return self.do_wait(EC.visibility_of_element_located(locator), true_or_false_for_visible_or_not, timeout)

    def wait_until_url_contains(self, url_sub_string, true_or_false_for_contains_or_not, timeout=2):
        return self.do_wait(EC.url_contains(url_sub_string), true_or_false_for_contains_or_not, timeout)

    def wait_until_alert_is_present(self, true_or_false_for_present_or_not, timeout=2):
        return self.do_wait(EC.alert_is_present(), true_or_false_for_present_or_not, timeout)

    # element actions
    def pick_in_combobox(self, combobox_locator, item_value, true_to_hit_enter_after_tab=False):
        combobox_element = self.driver.find_element(*combobox_locator)
        combobox_element.click()
        combobox_element_input = combobox_element.find_element_by_css_selector("input")
        # it is crutch, I know
        for i in range(15):
            combobox_element_input.send_keys(Keys.DELETE)
        for i in range(15):
            combobox_element_input.send_keys(Keys.BACKSPACE)
        combobox_element_input.send_keys(item_value)
        combobox_element_input.send_keys(Keys.TAB)
        if true_to_hit_enter_after_tab:
            combobox_element_input.send_keys(Keys.ENTER)

    def alert_wait_and_confirm(self, timeout=2):
        if self.wait_until_alert_is_present(True, timeout):
            self.driver.switch_to.alert.accept()
        self.wait_until_alert_is_present(False, timeout)
