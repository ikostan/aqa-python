from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject


class FlagContainerPageObject(BasePageObject):
    FLAG_CONTAINER = (By.ID, "aui-flag-container")
    FULL_MESSAGE = (By.CSS_SELECTOR, " .aui-message.closeable.aui-message-success.aui-will-close")
    ISSUE_CREATED_KEYS = (By.CSS_SELECTOR, " .issue-created-key.issue-link")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_until_flag_is_shown(self, timeout=3):
        return self.wait_until_element_is_present(self.FLAG_CONTAINER, timeout)

    def get_flag_element(self):
        return self.driver.find_element(*self.FLAG_CONTAINER)

    def get_full_message(self):
        return self.get_flag_element().find_element(*self.FULL_MESSAGE).text

    def get_new_issue_data(self):
        issue_keys_element = self.get_flag_element().find_element(*self.ISSUE_CREATED_KEYS)
        key = issue_keys_element.get_attribute("data-issue-key")
        link = issue_keys_element.get_attribute("href")
        summary = self.slice_off_substring(issue_keys_element.text, key + " - ")
        return {"key": key, "link": link, "summary": summary}
