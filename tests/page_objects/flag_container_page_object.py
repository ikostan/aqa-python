from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject


class FlagContainerPageObject(BasePageObject):
    FLAG_CONTAINER = (By.ID, "aui-flag-container")
    ISSUE_KEYS = (By.CSS_SELECTOR, " .issue-created-key.issue-link")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_until_flag_is_shown(self, timeout=3):
        return self.wait_until_element_is_present(self.FLAG_CONTAINER, timeout)

    def get_new_issue_data(self):
        issue_keys_element = self.driver.find_element(*self.FLAG_CONTAINER).find_element(*self.ISSUE_KEYS)
        key = issue_keys_element.get_attribute("data-issue-key")
        link = issue_keys_element.get_attribute("href")
        summary = self.slice_off_substring(issue_keys_element.text, key + " - ")
        return {"key": key, "link": link, "summary": summary}
