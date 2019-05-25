import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModalNoFixtures
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject


@pytest.mark.ui
class TestSearchIssue:
    created_issues = []
    ISSUE_PROJECT = "Webinar (WEBINAR)"
    ISSUE_TYPE = "Bug"
    ISSUE_SUMMARY = "Issue Should Be Updated #WDN1"
    ISSUE_DESCRIPTION = "Description of the <Issue Should Be Updated #WDN1>"
    ISSUE_PRIORITY = "Medium"

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
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
        self.browse_issue_page = BrowseIssuePageObject(self.driver, self.created_issues[0])

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
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
        self.browse_issue_page.open_page_by_url()

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @allure.title("JIRA. Issue summary is updated")
    def test_update_issue_summary(self):
        with allure.step("Update summary by valid value"):
            issue_summary_new = "Issue That Has Been Updated #WDN1"
            self.browse_issue_page.issue_details.update_summary(issue_summary_new)
        with allure.step("Refresh the page"):
            self.driver.refresh()
        with allure.step("Check the updated summary value"):
            assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_new

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @allure.title("JIRA. Issue priority is updated")
    def test_update_issue_priority(self):
        with allure.step("Select another priority"):
            issue_priority_new = "Highest"
            self.browse_issue_page.issue_details.select_priority(issue_priority_new)
        with allure.step("Refresh the page"):
            self.driver.refresh()
        with allure.step("Check the updated priority value"):
            assert self.browse_issue_page.issue_details.get_issue_priority() == issue_priority_new

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @allure.title("JIRA. Issue assignee is updated")
    def test_update_issue_assignee(self):
        with allure.step("Select another assignee"):
            issue_assignee_new = self.browse_issue_page.issue_details.USER_LOGIN
            self.browse_issue_page.issue_details.select_assignee(issue_assignee_new)
        with allure.step("Refresh the page"):
            self.driver.refresh()
        with allure.step("Check the updated assignee value"):
            assert self.browse_issue_page.issue_details.get_issue_assignee() == issue_assignee_new

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @allure.title("JIRA. Issue summary is not updated if inputted string is longer than 256 char")
    def test_update_issue_summary_256(self):
        with allure.step("Update summary by invalid value"):
            issue_summary_original = self.browse_issue_page.issue_details.get_issue_summary()
            issue_summary_new = "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456"
            self.browse_issue_page.issue_details.update_summary(issue_summary_new)
            error_message = self.browse_issue_page.issue_details.get_issue_summary_error()
            self.browse_issue_page.issue_details.click_summary_cancel()
        with allure.step("Refresh the page"):
            self.driver.refresh()
        with allure.step("Check the original summary value wasn't changed"):
            assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_original
        with allure.step("Check the proper error message is shown"):
            assert error_message == "Summary must be less than 255 characters."

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @allure.title("JIRA. Issue summary is not updated if new value is empty string")
    def test_update_issue_summary_empty(self):
        with allure.step("Update summary by invalid value"):
            issue_summary_original = self.browse_issue_page.issue_details.get_issue_summary()
            issue_summary_new = ""
            self.browse_issue_page.issue_details.update_summary(issue_summary_new, True)
            error_message = self.browse_issue_page.issue_details.get_issue_summary_error()
            self.browse_issue_page.issue_details.click_summary_cancel()
        with allure.step("Refresh the page"):
            self.driver.refresh()
        with allure.step("Check the original summary value wasn't changed"):
            assert self.browse_issue_page.issue_details.get_issue_summary() == issue_summary_original
        with allure.step("Check the proper error message is shown"):
            assert error_message == "You must specify a summary of the issue."
