import pytest
import allure
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModal
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject


@pytest.mark.ui
class TestCreateIssue:
    created_issues = []

    @pytest.fixture(scope="module", autouse=True)
    def driver(self, login_and_get_driver):
        driver = login_and_get_driver
        yield driver
        for issue in self.created_issues:
            driver.fullscreen_window()
            browse_issue_page = BrowseIssuePageObject(driver, issue)
            browse_issue_page.open_page_by_url()
            browse_issue_page.issue_details.delete_issue()

    @pytest.fixture(autouse=True)
    def objects(self, driver):
        dashboard = DashboardPageObject(driver)
        modal = CreateIssueModal(driver)
        dashboard.open_page()
        i = 0
        while i < 3 and modal.is_modal_existing() is False:
            dashboard.header_toolbar.click_create_button()
            modal.wait_until_modal_is_opened(5)
            i += 1
        yield {"dashboard": dashboard, "modal": modal}
        if modal.is_modal_existing(): modal.cancel_creation()

    @allure.title("JIRA. Create issue - positive (fixtures)")
    @pytest.mark.parametrize(
        "project, issue_type, summary, description, priority, error_message_expect, is_modal_closed_expect", [
            ("Webinar (WEBINAR)", "Bug", "Test summary (QA) Without Description (fixtures)", None, "Medium", None, True),
            ("Webinar (WEBINAR)", "Bug", "Test summary (QA) With Description (fixtures)", "*Test description*",
             "Medium", None, True),
            ("Webinar (WEBINAR)", "Bug",
             "fixtures_yes_456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345",
             None, "Medium", None, True),
        ])
    def test_create_issue_positive(self, objects, project, issue_type, summary, description, priority,
                                   error_message_expect, is_modal_closed_expect):
        self.dashboard = objects["dashboard"]
        self.modal = objects["modal"]
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


    @allure.title("JIRA. Create issue - negative (fixtures)")
    @pytest.mark.parametrize(
        "project, issue_type, summary, description, priority, error_message_expect, is_modal_closed_expect", [
            ("Webinar (WEBINAR)", "Bug", None, None, "Medium", "You must specify a summary of the issue.", False),
            ("Webinar (WEBINAR)", "Bug",
             "fixtures_yes_456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456",
             None, "Medium", "Summary must be less than 255 characters.", False),
        ])
    def test_create_issue_negative(self, objects, project, issue_type, summary, description, priority,
                                   error_message_expect, is_modal_closed_expect):
        self.modal = objects["modal"]
        with allure.step("Populate the issue form and submit"):
            self.modal.populate_fields_and_click_create(project, issue_type, summary, description, priority)
            self.modal.wait_until_modal_is_not_opened(2)
        with allure.step("Check the correct error message is shown"):
            assert self.modal.get_issue_summary_error_message() == error_message_expect
        with allure.step("Check the issue form wasn't closed"):
            assert self.modal.is_modal_existing() is not is_modal_closed_expect
