import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModal
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject


@pytest.mark.ui
class TestUpdateIssue:
    created_issues = []
    ISSUE_PROJECT = "Webinar (WEBINAR)"
    ISSUE_TYPE = "Bug"
    ISSUE_SUMMARY_BASE = "Issue Should Be Updated #WDN1"
    ISSUE_DESCRIPTION = "Description of the <Issue Should Be Updated #WDN1>"
    ISSUE_PRIORITY = "Medium"

    def setup_class(self):
        with allure.step("Login, get driver and create an issue"):
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
            self.login = LoginPageObject(self.driver)
            self.login.enter_site_as_test_user()
            self.dashboard = DashboardPageObject(self.driver)

    def teardown_class(self):
        for issue in self.created_issues:
            self.driver.fullscreen_window()
            self.browse_issue_page = BrowseIssuePageObject(self.driver, issue)
            self.browse_issue_page.open_page_by_url()
            self.browse_issue_page.issue_details.delete_issue()
        try:
            self.driver.close()
        except Exception as e:
            print(e)
            pass

    def create_original_issue(self, original_summary):
        with allure.step("Open the dashboard page"):
            self.dashboard.open_page()
        with allure.step("Open the Create issue modal"):
            self.modal = CreateIssueModal(self.driver)
            i = 0
            while i < 3 and self.modal.is_modal_existing() is False:
                self.dashboard.header_toolbar.click_create_button()
                self.modal.wait_until_modal_is_opened(5)
                i += 1
        with allure.step("Create the new original issue"):
            self.modal.populate_fields_and_click_create(self.ISSUE_PROJECT, self.ISSUE_TYPE, original_summary,
                                                        self.ISSUE_DESCRIPTION, self.ISSUE_PRIORITY)
            self.dashboard.flag.wait_until_flag_is_shown()
            new_issue_link = self.dashboard.flag.get_new_issue_data()["link"]
            self.created_issues.append(new_issue_link)
            self.modal.wait_until_modal_is_not_opened(10)
        with allure.step("Open the issue page and update it by valid values"):
            self.browse_issue_page = BrowseIssuePageObject(self.driver, new_issue_link)
            self.browse_issue_page.open_page_by_url()

    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    @allure.title("JIRA. Issue summary is updated")
    def test_update_issue_summary(self):
        with allure.step("Create original issue"):
            original_summary = self.ISSUE_SUMMARY_BASE + " (update summary)"
            self.create_original_issue(original_summary)
        with allure.step("Update issue"):
            issue_summary_new = "Issue That Has Been Updated #WDN1"
            self.browse_issue_page.issue_details.update_summary(issue_summary_new)
        with allure.step("Check update"):
            assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_new

    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    @allure.title("JIRA. Issue priority is updated")
    def test_update_issue_priority(self):
        with allure.step("Create original issue"):
            original_summary = self.ISSUE_SUMMARY_BASE + " (update priority)"
            self.create_original_issue(original_summary)
        with allure.step("Update issue"):
            issue_priority_new = "Highest"
            self.browse_issue_page.issue_details.select_priority(issue_priority_new)
        with allure.step("Check update"):
            assert self.browse_issue_page.issue_details.get_issue_priority() == issue_priority_new

    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    @allure.title("JIRA. Issue assignee is updated")
    def test_update_issue_assignee(self):
        with allure.step("Create original issue"):
            original_summary = self.ISSUE_SUMMARY_BASE + " (update assignee)"
            self.create_original_issue(original_summary)
        with allure.step("Update issue"):
            issue_assignee_new = self.browse_issue_page.issue_details.USER_LOGIN
            self.browse_issue_page.issue_details.select_assignee(issue_assignee_new)
        with allure.step("Check update"):
            assert self.browse_issue_page.issue_details.get_issue_assignee() == issue_assignee_new

    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    @allure.title("JIRA. Issue summary is not updated if inputted string is longer than 256 char")
    def test_update_issue_summary_256(self):
        with allure.step("Create original issue"):
            original_summary = self.ISSUE_SUMMARY_BASE + " (update summary by 256 chars name)"
            self.create_original_issue(original_summary)
        with allure.step("Replace name by empty value"):
            issue_summary_new = "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456"
            self.browse_issue_page.issue_details.update_summary(issue_summary_new)
        with allure.step("Get error message and cancel updates"):
            error_message = self.browse_issue_page.issue_details.get_issue_summary_error()
            self.browse_issue_page.issue_details.click_summary_cancel()
        with allure.step("Check the original summary value wasn't changed"):
            assert self.browse_issue_page.issue_details.get_issue_summary() == original_summary
        with allure.step("Check the proper error message is shown"):
            assert error_message == "Summary must be less than 255 characters."

    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    @allure.title("JIRA. Issue summary is not updated if new value is empty string")
    def test_update_issue_summary_empty(self):
        with allure.step("Create original issue"):
            original_summary = self.ISSUE_SUMMARY_BASE + " (update summary by empty value)"
            self.create_original_issue(original_summary)
        with allure.step("Replace name by empty value"):
            self.browse_issue_page.issue_details.update_summary("", True)
        with allure.step("Get error message and cancel updates"):
            error_message = self.browse_issue_page.issue_details.get_issue_summary_error()
            self.browse_issue_page.issue_details.click_summary_cancel()
        with allure.step("Check the original summary value wasn't changed"):
            assert self.browse_issue_page.issue_details.get_issue_summary() == original_summary
        with allure.step("Check the proper error message is shown"):
            assert error_message == "You must specify a summary of the issue."
