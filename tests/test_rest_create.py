import pytest
import allure
from tests.rest.rest_issue_create import RestIssueCreate
from tests.rest.rest_issue_get import RestIssueGet


@pytest.mark.rest
class TestRestCreate:

    @pytest.fixture(scope="module", autouse=True)
    def create(self, rest_set_session):
        cookie = rest_set_session
        return {"create": RestIssueCreate(cookie), "get": RestIssueGet(cookie)}

    @allure.title("REST JIRA. Create (positive)")
    @pytest.mark.parametrize("summary, issue_type, project, description, assignee, priority, status",
                             [
                                 ("Test Issue Summary1", "Bug", "default", "Test Issue Description", "default",
                                  "Medium", 201),
                                 ("Test Issue Summary2", "Bug", "default", None, None, None, 201),
                                 ("123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345",
                                 "Bug", "default", None, None, None, 201),
                             ])
    def test_create_issue_positive(self, create, summary, issue_type, project, description, assignee, priority, status):
        with allure.step("Setup request"):
            rest_create = create["create"]
            rest_get = create["get"]
            if project == "default": project = rest_create.JIRA_PROJECT_KEY
            if assignee == "default": assignee = rest_create.JIRA_USER_NAME
        with allure.step("Send request"):
            r = rest_create.rest_jira_create_issue(summary, issue_type, project, description, assignee, priority)
        with allure.step("Check the status code"):
            assert r.status_code == status
        with allure.step("Check the created values"):
            issue = rest_get.get_issue(r.json()["id"])
            assert issue["summary"] == summary
            assert issue["issue_type"] == issue_type
            assert issue["project"] == project
            assert issue["description"] == description
            assert issue["assignee"] == assignee
            assert issue["priority"] is not None

    @allure.title("REST JIRA. Create (negative)")
    @pytest.mark.parametrize("summary, issue_type, project, description, assignee, priority, status",
                             [
                                 ("123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456",
                                 "Bug", "default", None, None, None, 400),
                                 ("Test Issue Summary5", "Bug", None, None, None, None, 400),
                                 (None, "Bug", "default", None, None, None, 400),
                                 ("Test Issue Summary7", None, "default", None, None, None, 400),
                             ])
    def test_create_issue_negative(self, create, summary, issue_type, project, description, assignee, priority, status):
        with allure.step("Setup request"):
            rest_create = create["create"]
            if project == "default": project = rest_create.JIRA_PROJECT_KEY
            if assignee == "default": assignee = rest_create.JIRA_USER_NAME
        with allure.step("Send request"):
            r = rest_create.rest_jira_create_issue(summary, issue_type, project, description, assignee, priority)
        with allure.step("Check the status code"):
            assert r.status_code == status
