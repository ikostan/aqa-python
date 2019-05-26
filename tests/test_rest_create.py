import pytest
import allure
from tests.rest.rest_issue_create import RestIssueCreate


@pytest.mark.rest
class TestRestCreate:

    @pytest.fixture(scope="module", autouse=True)
    def create(self, rest_set_session):
        cookie = rest_set_session
        return RestIssueCreate(cookie)

    @allure.title("REST JIRA. Create")
    @pytest.mark.parametrize("summary, issue_type, project_key, description, assignee_name, priority_name, status_code",
                             [
                                 ("Test Issue Summary1", "Bug", "default", "Test Issue Description", "default",
                                  "Medium", 201),
                                 ("Test Issue Summary2", "Bug", "default", None, None, None, 201),
                                 ("123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345",
                                  "Bug", "default", None, None, None, 201),
                                 ("123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456",
                                  "Bug", "default", None, None, None, 400),
                                 ("Test Issue Summary5", "Bug", None, None, None, None, 400),
                                 (None, "Bug", "default", None, None, None, 400),
                                 ("Test Issue Summary7", None, "default", None, None, None, 400),
                             ])
    def test_create_issue(self, create, summary, issue_type, project_key, description, assignee_name, priority_name,
                          status_code):
        with allure.step("Setup request"):
            if project_key == "default": project_key = create.JIRA_PROJECT_KEY
            if assignee_name == "default": assignee_name = create.JIRA_USER_NAME
        with allure.step("Send request"):
            r = create.rest_jira_create_issue(summary, issue_type, project_key, description, assignee_name, priority_name)
        with allure.step("Check the status code"):
            assert r.status_code == status_code
