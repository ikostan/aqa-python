import pytest
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModal
from tests.page_objects.browse_issue_page_object import BrowseIssuePageObject


class TestCreateIssue:
    @pytest.fixture(autouse=True)
    def setup_method(self, login_and_get_driver):
        self.driver = login_and_get_driver
        self.dashboard_page = DashboardPageObject(self.driver)
        self.created_issues = []
        self.dashboard_page.open_page()

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
    def test_create_issue(self, project, issue_type, summary, description, priority):
        self.dashboard_page.header_toolbar.click_create_button()
        self.create_issue_modal = CreateIssueModal(self.driver)
        self.create_issue_modal.wait_until_modal_is_opened(5)
        self.create_issue_modal.populate_fields_and_click_create(project, issue_type, summary, description, priority)
        self.create_issue_modal.wait_until_modal_is_not_opened()
        self.dashboard_page.flag.wait_until_flag_is_shown()
        self.created_issues.append(self.dashboard_page.flag.get_new_issue_data()["link"])
        assert summary == self.dashboard_page.flag.get_new_issue_data()["summary"]

    def teardown_method(self):
        for issue in self.created_issues:
            browse_issue_page = BrowseIssuePageObject(self.driver, issue)
            browse_issue_page.open_page_by_url()
            browse_issue_page.issue_details.delete_issue()
        self.driver.close()
