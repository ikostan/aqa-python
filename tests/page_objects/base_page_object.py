from tests.credentials import credentials
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePageObject:
    BASE_URL = "https://jira.hillel.it"
    USER_LOGIN = credentials.user_login
    USER_PASSWORD = credentials.user_password

    def __init__(self, driver):
        self.driver = driver

    def get_user_login(self):
        return self.USER_LOGIN

    def get_user_password(self):
        return self.USER_PASSWORD

    def get_base_url(self):
        return self.BASE_URL

    def is_element_present(self, element):
        return EC.presence_of_element_located(element)

    def wait_until_element_is_present(self, element, timeout=5):
        try:
            got_element = WebDriverWait(self.driver, timeout).until(self.is_element_present(element))
            result = got_element.is_displayed()
        except:
            result = False
        finally:
            return result
