import pytest
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModal
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject


class TestCreateIssue:
    created_issues = []

    @pytest.fixture(scope="module", autouse=True)
    def before_after(self, login_and_get_driver):
        driver = login_and_get_driver
        dashboard_page = DashboardPageObject(driver)
        yield {"driver": driver, "dashboard": dashboard_page}
        for issue in self.created_issues:
            driver.fullscreen_window()
            browse_issue_page = BrowseIssuePageObject(driver, issue)
            browse_issue_page.open_page_by_url()
            browse_issue_page.issue_details.delete_issue()

    @pytest.mark.parametrize("project, issue_type, summary, description, priority", [
        ("Webinar (WEBINAR)", "Bug", "Test summary (QA) 1", "*Test description (should be removed)*",
         "Medium"),
        ("Webinar (WEBINAR)", "Bug", "Test summary (QA) 2", "*Test description (should be removed)*",
         "Medium"),
        ("Webinar (WEBINAR)", "Bug", "Test summary (QA) 3", "*Test description (should be removed)*",
         "Medium"),
        ("Webinar (WEBINAR)", "Bug", "Test summary (QA) 4", "*Test description (should be removed)*",
         "Medium")
    ])
    def test_create_issue(self, before_after, project, issue_type, summary, description, priority):
        self.driver = before_after["driver"]
        self.dashboard = before_after["dashboard"]
        self.dashboard.open_page()
        self.dashboard.header_toolbar.click_create_button()
        self.create_issue_modal = CreateIssueModal(self.driver)
        self.create_issue_modal.wait_until_modal_is_opened(5)
        self.create_issue_modal.populate_fields_and_click_create(project, issue_type, summary, description, priority)
        self.create_issue_modal.wait_until_modal_is_not_opened()
        self.dashboard.flag.wait_until_flag_is_shown()
        self.created_issues.append(self.dashboard.flag.get_new_issue_data()["link"])
        assert summary == self.dashboard.flag.get_new_issue_data()["summary"]
