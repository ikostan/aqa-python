import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModal
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject


@pytest.mark.ui
class TestCreateIssue:
    created_issues = []

    def setup_class(self):
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

    def setup_method(self):
        self.dashboard.open_page()
        self.modal = CreateIssueModal(self.driver)
        i = 0
        while i < 3 and self.modal.is_modal_existing() is False:
            self.dashboard.header_toolbar.click_create_button()
            self.modal.wait_until_modal_is_opened(5)
            i += 1

    def teardown_method(self):
        if self.modal.is_modal_existing():
            self.modal.cancel_creation()

    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @allure.title("JIRA. Create issue - positive (no fixtures)")
    @pytest.mark.parametrize(
        "project, issue_type, summary, description, priority, error_message_expect, is_modal_closed_expect", [
            ("Webinar (WEBINAR)", "Bug", "Test summary (QA) Without Description (no fixtures)", None, "Medium", None, True),
            ("Webinar (WEBINAR)", "Bug", "Test summary (QA) With Description (no fixtures)", "*Test description*",
             "Medium", None, True),
            ("Webinar (WEBINAR)", "Bug",
             "fixtures_no_3456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345",
             None, "Medium", None, True),
        ])
    def test_create_issue_positive(self, project, issue_type, summary, description, priority, error_message_expect,
                                   is_modal_closed_expect):
        with allure.step("Populate the issue form and submit"):
            self.modal.populate_fields_and_click_create(project, issue_type, summary, description, priority)
        with allure.step("Wait for successful flag and get issue data"):
            self.dashboard.flag.wait_until_flag_is_shown()
            self.created_issues.append(self.dashboard.flag.get_new_issue_data()["link"])
        with allure.step("Check the correct issue summary in the flag"):
            assert self.dashboard.flag.get_new_issue_data()["summary"] == summary
        with allure.step("Check the issue form is closed"):
            assert self.modal.wait_until_modal_is_not_opened(5) == is_modal_closed_expect
        with allure.step("Check the error message existing"):
            assert self.modal.get_issue_summary_error_message() is error_message_expect

    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @allure.title("JIRA. Create issue - negative (no fixtures)")
    @pytest.mark.parametrize(
        "project, issue_type, summary, description, priority, error_message_expect, is_modal_closed_expect", [
            ("Webinar (WEBINAR)", "Bug", None, None, "Medium", "You must specify a summary of the issue.", False),
            ("Webinar (WEBINAR)", "Bug",
             "fixtures_no_3456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456",
             None, "Medium", "Summary must be less than 255 characters.", False),
        ])
    def test_create_issue_negative(self, project, issue_type, summary, description, priority, error_message_expect,
                                   is_modal_closed_expect):
        with allure.step("Populate the issue form and submit"):
            self.modal.populate_fields_and_click_create(project, issue_type, summary, description, priority)
            self.modal.wait_until_modal_is_not_opened(3)
        with allure.step("Check the correct error message is shown"):
            assert self.modal.get_issue_summary_error_message() == error_message_expect
        with allure.step("Check the issue form wasn't closed"):
            assert self.modal.is_modal_existing() is not is_modal_closed_expect
