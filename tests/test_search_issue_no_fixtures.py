import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModalNoFixtures
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject
from tests.page_objects.search_page_object import SearchPageObject


class TestSearchIssue:
    created_issues = []
    ISSUE_PROJECT = "Webinar (WEBINAR)"
    ISSUE_TYPE = "Bug"
    ISSUE_SUMMARY = "Checking The Searching Feature With The Selenium Python"
    ISSUE_DESCRIPTION = "Description of the <Checking Searching Feature With Selenium Python AQA>"
    ISSUE_PRIORITY = "Medium"

    def setup_class(self):
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        self.login = LoginPageObject(self.driver)
        self.login.enter_site_as_test_user()
        self.dashboard = DashboardPageObject(self.driver)
        self.dashboard.open_page()
        self.dashboard.header_toolbar.click_create_button()
        self.create_issue_modal = CreateIssueModalNoFixtures(self.driver)
        self.create_issue_modal.wait_until_modal_is_opened(5)
        self.create_issue_modal.populate_fields_and_click_create(self.ISSUE_PROJECT, self.ISSUE_TYPE,
                                                                 self.ISSUE_SUMMARY, self.ISSUE_DESCRIPTION,
                                                                 self.ISSUE_PRIORITY)
        self.dashboard.flag.wait_until_flag_is_shown()
        self.created_issues.append(self.dashboard.flag.get_new_issue_data()["link"])
        self.create_issue_modal.wait_until_modal_is_not_opened(2)

    def teardown_class(self):
        for issue in self.created_issues:
            self.driver.fullscreen_window()
            self.browse_issue_page = BrowseIssuePageObject(self.driver, issue)
            self.browse_issue_page.open_page_by_url()
            self.browse_issue_page.issue_details.delete_issue()
        try:
            self.driver.close()
            # driver.quit()
        except:
            pass

    def setup_method(self):
        self.dashboard.open_page()

    @pytest.mark.parametrize("case_method", [None, "lower", "upper"])
    def test_search_issue(self, case_method):
        if case_method is None:
            search_string = self.ISSUE_SUMMARY
        elif case_method == "lower":
            search_string = self.ISSUE_SUMMARY.lower()
        elif case_method == "upper":
            search_string = self.ISSUE_SUMMARY.upper()
        self.dashboard.header_toolbar.populate_search_and_submit(search_string)
        self.search_page = SearchPageObject(self.driver)
        self.search_page.wait_until_page_is_opened()
        assert self.search_page.is_result_item_existing_by_name(self.ISSUE_SUMMARY) is True
        assert self.search_page.issue.get_issue_summary() == self.ISSUE_SUMMARY

    def test_search_issue_not_found(self):
        self.dashboard.header_toolbar.populate_search_and_submit("incorrect_search_request_should_not_be_found")
        self.search_page = SearchPageObject(self.driver)
        self.search_page.wait_until_page_is_opened()
        assert self.search_page.wait_until_no_result_message_is_opened(3) is True
        assert self.search_page.wait_until_result_list_is_opened(1) is False
        assert self.search_page.issue.wait_until_panel_is_opened(1) is False
