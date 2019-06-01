import pytest
import allure
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModalNoFixtures
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject


@pytest.mark.ui
class TestCreateIssue:
    created_issues = []

    @pytest.fixture(scope="module", autouse=True)
    def before_all_and_after_all(self, login_and_get_driver):
        driver = login_and_get_driver
        dashboard_page = DashboardPageObject(driver)
        yield {"driver": driver, "dashboard": dashboard_page}
        for issue in self.created_issues:
            driver.fullscreen_window()
            browse_issue_page = BrowseIssuePageObject(driver, issue)
            browse_issue_page.open_page_by_url()
            browse_issue_page.issue_details.delete_issue()

    def before_each(self, before_after, project, issue_type, summary, description, priority):
        self.driver = before_after["driver"]
        self.dashboard = before_after["dashboard"]
        self.create_issue_modal = CreateIssueModalNoFixtures(self.driver)
        with allure.step("Open the Dashboard then open Create issue modal"):
        # with allure.step("Open the Dashboard and click the Create button"):
            self.dashboard.open_page()
            i = 0
            while i < 3 and self.create_issue_modal.is_modal_existing() is False:
                self.dashboard.header_toolbar.click_create_button()
                self.create_issue_modal.wait_until_modal_is_opened(5)
                i += 1
            # self.dashboard.header_toolbar.click_create_button()
        # with allure.step("Populate issue form and submit"):
            # self.create_issue_modal.wait_until_modal_is_opened(5)
            self.create_issue_modal.populate_fields_and_click_create(project, issue_type, summary, description, priority)

    @allure.title("JIRA. Create issue - positive (fixtures)")
    @pytest.mark.parametrize(
        "project, issue_type, summary, description, priority, error_message_expect, is_modal_closed_expect", [
            ("Webinar (WEBINAR)", "Bug", "Test summary (QA) Without Description", None, "Medium", None, True),
            ("Webinar (WEBINAR)", "Bug", "Test summary (QA) With Description", "*Test description*",
             "Medium", None, True),
            ("Webinar (WEBINAR)", "Bug",
             "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345",
             None, "Medium", None, True),
        ])
    def test_create_issue_positive(self, before_all_and_after_all, project, issue_type, summary, description, priority,
                                   error_message_expect, is_modal_closed_expect):
        with allure.step("Test setup:"):
            self.before_each(before_all_and_after_all, project, issue_type, summary, description, priority)
        with allure.step("Wait for successful flag and get issue data"):
            self.dashboard.flag.wait_until_flag_is_shown()
            self.created_issues.append(self.dashboard.flag.get_new_issue_data()["link"])
        with allure.step("Check the correct issue summary in the flag"):
            assert self.dashboard.flag.get_new_issue_data()["summary"] == summary
        with allure.step("Check the issue form is closed"):
            assert self.create_issue_modal.wait_until_modal_is_not_opened(2) == is_modal_closed_expect
        with allure.step("Check the error message existing"):
            assert self.create_issue_modal.get_issue_summary_error_message() == error_message_expect

    @allure.title("JIRA. Create issue - negative (no fixtures)")
    @pytest.mark.parametrize(
        "project, issue_type, summary, description, priority, error_message_expect, is_modal_closed_expect", [
            ("Webinar (WEBINAR)", "Bug", None, None, "Medium", "You must specify a summary of the issue.", False),
            ("Webinar (WEBINAR)", "Bug",
             "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456",
             None, "Medium", "Summary must be less than 255 characters.", False),
        ])
    def test_create_issue_negative(self, before_all_and_after_all, project, issue_type, summary, description, priority,
                                   error_message_expect, is_modal_closed_expect):
        with allure.step("Test setup:"):
            self.before_each(before_all_and_after_all, project, issue_type, summary, description, priority)
        with allure.step("Wait for error message and cancel the creation"):
            is_modal_closed_actual = self.create_issue_modal.wait_until_modal_is_not_opened(1)
            error_message_actual = self.create_issue_modal.get_issue_summary_error_message()
            if self.create_issue_modal.is_modal_existing():
                self.create_issue_modal.cancel_creation()
        with allure.step("Check the correct error message is shown"):
            assert error_message_actual == error_message_expect
        with allure.step("Check the issue form wasn't closed"):
            assert is_modal_closed_actual == is_modal_closed_expect
