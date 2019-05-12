from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModalNoFixtures
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject


class TestSearchIssue:
    created_issues = []
    ISSUE_PROJECT = "Webinar (WEBINAR)"
    ISSUE_TYPE = "Bug"
    ISSUE_SUMMARY = "Issue Should Be Updated #WDN1"
    ISSUE_DESCRIPTION = "Description of the <Issue Should Be Updated #WDN1>"
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
                                                                 self.ISSUE_SUMMARY,
                                                                 self.ISSUE_DESCRIPTION, self.ISSUE_PRIORITY)
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
        self.browse_issue_page = BrowseIssuePageObject(self.driver, self.created_issues[0])
        self.browse_issue_page.open_page_by_url()

    def test_update_issue_summary_255(self):
        issue_summary_new = "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345"
        self.browse_issue_page.issue_details.update_summary(issue_summary_new)
        self.driver.refresh()
        assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_new

    def test_update_issue_summary(self):
        issue_summary_new = "Issue That Has Been Updated #WDN1"
        self.browse_issue_page.issue_details.update_summary(issue_summary_new)
        self.driver.refresh()
        assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_new

    def test_update_issue_priority(self):
        issue_priority_new = "Highest"
        self.browse_issue_page.issue_details.select_priority(issue_priority_new)
        self.driver.refresh()
        assert self.browse_issue_page.issue_details.get_issue_priority() == issue_priority_new

    def test_update_issue_assignee(self):
        issue_assignee_new = self.browse_issue_page.issue_details.USER_LOGIN
        self.browse_issue_page.issue_details.select_assignee(issue_assignee_new)
        self.driver.refresh()
        assert self.browse_issue_page.issue_details.get_issue_assignee() == issue_assignee_new

    def test_update_issue_summary_256(self):
        issue_summary_original = self.browse_issue_page.issue_details.get_issue_summary()
        issue_summary_new = "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456"
        self.browse_issue_page.issue_details.update_summary(issue_summary_new)
        error_message = self.browse_issue_page.issue_details.get_issue_summary_error()
        self.browse_issue_page.issue_details.click_summary_cancel()
        self.driver.refresh()
        assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_original
        assert error_message == "Summary must be less than 255 characters."

    def test_update_issue_summary_empty(self):
        issue_summary_original = self.browse_issue_page.issue_details.get_issue_summary()
        issue_summary_new = ""
        self.browse_issue_page.issue_details.update_summary(issue_summary_new, True)
        error_message = self.browse_issue_page.issue_details.get_issue_summary_error()
        self.browse_issue_page.issue_details.click_summary_cancel()
        self.driver.refresh()
        assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_original
        assert error_message == "You must specify a summary of the issue."
