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
    ISSUE_SUMMARY = "Issue Should Be Updated #WDN1"
    ISSUE_DESCRIPTION = "Description of the <Issue Should Be Updated #WDN1>"
    ISSUE_PRIORITY = "Medium"

    def setup_class(self):
        with allure.step("Login, get driver and create an issue"):
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
            self.login = LoginPageObject(self.driver)
            self.login.enter_site_as_test_user()
            self.dashboard = DashboardPageObject(self.driver)
            self.dashboard.open_page()
            self.modal = CreateIssueModal(self.driver)
            i = 0
            while i < 3 and self.modal.is_modal_existing() is False:
                self.dashboard.header_toolbar.click_create_button()
                self.modal.wait_until_modal_is_opened(5)
                i += 1
            self.modal.populate_fields_and_click_create(self.ISSUE_PROJECT, self.ISSUE_TYPE, self.ISSUE_SUMMARY,
                                                        self.ISSUE_DESCRIPTION, self.ISSUE_PRIORITY)
            self.dashboard.flag.wait_until_flag_is_shown()
            self.created_issues.append(self.dashboard.flag.get_new_issue_data()["link"])
            self.modal.wait_until_modal_is_not_opened(2)
        with allure.step("Open the issue page and update it by valid values"):
            self.browse_issue_page = BrowseIssuePageObject(self.driver, self.created_issues[0])
            self.browse_issue_page.open_page_by_url()
            self.ISSUE_SUMMARY_NEW = "Issue That Has Been Updated #WDN1"
            self.ISSUE_PRIORITY_NEW = "Highest"
            self.ISSUE_ASSIGNEE_NEW = self.browse_issue_page.issue_details.USER_LOGIN
            self.browse_issue_page.issue_details.update_summary(self.ISSUE_SUMMARY_NEW)
            self.browse_issue_page.issue_details.select_priority(self.ISSUE_PRIORITY_NEW)
            self.browse_issue_page.issue_details.select_assignee(self.ISSUE_ASSIGNEE_NEW)
            self.browse_issue_page.open_page_by_url()

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

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @allure.title("JIRA. Issue summary is updated")
    def test_update_issue_summary(self):
        assert self.browse_issue_page.issue_details.get_issue_summary() == self.ISSUE_SUMMARY_NEW

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @allure.title("JIRA. Issue priority is updated")
    def test_update_issue_priority(self):
        assert self.browse_issue_page.issue_details.get_issue_priority() == self.ISSUE_PRIORITY_NEW

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @allure.title("JIRA. Issue assignee is updated")
    def test_update_issue_assignee(self):
        assert self.browse_issue_page.issue_details.get_issue_assignee() == self.ISSUE_ASSIGNEE_NEW

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @allure.title("JIRA. Issue summary is not updated if inputted string is longer than 256 char")
    def test_update_issue_summary_256(self):
        with allure.step("Open the issue page and get original summary"):
            self.browse_issue_page.open_page_by_url()
            issue_summary_original = self.browse_issue_page.issue_details.get_issue_summary()
        with allure.step("Replace name by empty value"):
            issue_summary_new = "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456"
            self.browse_issue_page.issue_details.update_summary(issue_summary_new)
        with allure.step("Get error message and cancel updates"):
            error_message = self.browse_issue_page.issue_details.get_issue_summary_error()
            self.browse_issue_page.issue_details.click_summary_cancel()
        with allure.step("Check the original summary value wasn't changed"):
            assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_original
        with allure.step("Check the proper error message is shown"):
            assert error_message == "Summary must be less than 255 characters."

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @allure.title("JIRA. Issue summary is not updated if new value is empty string")
    def test_update_issue_summary_empty(self):
        with allure.step("Open the issue page and get original summary"):
            self.browse_issue_page.open_page_by_url()
            issue_summary_original = self.browse_issue_page.issue_details.get_issue_summary()
        with allure.step("Replace name by empty value"):
            self.browse_issue_page.issue_details.update_summary("", True)
        with allure.step("Get error message and cancel updates"):
            error_message = self.browse_issue_page.issue_details.get_issue_summary_error()
            self.browse_issue_page.issue_details.click_summary_cancel()
        with allure.step("Check the original summary value wasn't changed"):
            assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_original
        with allure.step("Check the proper error message is shown"):
            assert error_message == "You must specify a summary of the issue."
