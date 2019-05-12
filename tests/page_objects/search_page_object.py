from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject
from tests.page_objects.fragments.header_toolbar_fragment import HeaderToolbarFragment
from tests.page_objects.fragments.issue_details_fragment import IssueDetailsFragment


class SearchPageObject(BasePageObject):
    PAGE_TITLE = (By.CSS_SELECTOR, "h1.search-title[title='Search']")
    SEARCH_TOOLBAR = (By.CSS_SELECTOR, "form.aui.navigator-search")
    SEARCH_RESULTS_LIST = (By.CSS_SELECTOR, " .search-results")
    SEARCH_RESULTS_LIST_ITEM = (By.CSS_SELECTOR, " .search-results li")
    SEARCH_NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, " .no-results.no-results-message")

    def __init__(self, driver):
        super().__init__(driver)
        self.header_toolbar = HeaderToolbarFragment(driver)
        self.issue = IssueDetailsFragment(driver)

    def wait_until_page_is_opened(self, timeout=10):
        self.header_toolbar.wait_until_user_button_is_present(timeout)
        return self.wait_until_element_is_visible(self.SEARCH_TOOLBAR, True, timeout)

    def wait_until_result_list_is_opened(self, timeout=2):
        return self.wait_until_element_is_visible(self.SEARCH_RESULTS_LIST, True, timeout)

    def wait_until_no_result_message_is_opened(self, timeout=2):
        return self.wait_until_element_is_visible(self.SEARCH_NO_RESULTS_MESSAGE, True, timeout)

    def get_result_item_locator_by_name(self, issue_name):
        return (By.CSS_SELECTOR, " .search-results li[title='" + issue_name + "']")

    def is_result_item_existing_by_name(self, issue_name):
        return self.driver.find_element(*self.get_result_item_locator_by_name(issue_name)).is_displayed()
