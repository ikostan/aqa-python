import pytest
from selenium.webdriver.common.by import By
from tests.page_objects.dashboard_page_object import DashboardPageObject
from tests.page_objects.create_issue_modal_page_object import CreateIssueModal


class TestCreateIssue:
    @pytest.fixture(autouse=True)
    def setup_method(self, login_and_get_driver):
        self.driver = login_and_get_driver
        self.dashboard_page = DashboardPageObject(self.driver)
        self.dashboard_page.open_page()

    # @pytest.mark.parametrize("project, issue_type, summary, description, priority", [
    #     ("Webinar (Webinar)", "Bug", "Test summary (should be removed)", "*Test description (should be removed)*",
    #      "Medium")
    # ])
    # def test_create_issue(self, project, issue_type, summary, description, priority):
    #     self.dashboard_page.header_toolbar.click_create_button()
    #     self.create_issue_modal = CreateIssueModal(self.driver)
    #     self.create_issue_modal.wait_until_modal_is_opened(5)
    #     self.create_issue_modal.populate_fields_and_click_create(project, issue_type, summary, description, priority)
    #     self.create_issue_modal.wait_until_modal_is_not_opened()
    #     self.dashboard_page.flag.wait_until_flag_is_shown()
    #     assert summary == self.dashboard_page.flag.get_new_issue_data()["summary"]

    def teardown_method(self):
        self.driver.close()
