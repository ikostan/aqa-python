import pytest
import allure
from tests.rest.rest_issue_create import RestIssueCreate
from tests.rest.rest_issue_get import RestIssueGet
from tests.rest.rest_issue_delete import RestIssueDelete


@pytest.mark.rest
class TestRestCreate:

    created_issue_ids = []

    @pytest.fixture(scope="module", autouse=True)
    def rest_client(self, rest_set_session):
        cookie = rest_set_session
        yield {"create": RestIssueCreate(cookie), "get": RestIssueGet(cookie)}
        rest_delete = RestIssueDelete(cookie)
        rest_delete.delete_issues(self.created_issue_ids)


    @allure.title("REST JIRA. Create (positive)")
    @pytest.mark.parametrize("summary, issue_type, project, description, assignee, priority, status",
                             [
                                 ("Test Issue Summary1", "Bug", "default", "Test Issue Description", "default",
                                  "Medium", 201),
                                 ("Test Issue Summary2", "Bug", "default", None, None, None, 201),
                                 ("123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345",
                                 "Bug", "default", None, None, None, 201),
                             ])
    def test_create_issue_positive(self, rest_client, summary, issue_type, project, description, assignee, priority, status):
        with allure.step("Setup request"):
            rest_create = rest_client["create"]
            rest_get = rest_client["get"]
            if project == "default": project = rest_create.JIRA_PROJECT_KEY
            if assignee == "default": assignee = rest_create.JIRA_USER_NAME
        with allure.step("Send request"):
            r = rest_create.rest_jira_create_issue(summary, issue_type, project, description, assignee, priority)
            issue_id = r.json()["id"]
            self.created_issue_ids.append(issue_id)
        with allure.step("Check the status code"):
            assert r.status_code == status
        with allure.step("Check the created values"):
            issue = rest_get.get_issue(issue_id)
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
    def test_create_issue_negative(self, rest_client, summary, issue_type, project, description, assignee, priority, status):
        with allure.step("Setup request"):
            rest_create = rest_client["create"]
            if project == "default": project = rest_create.JIRA_PROJECT_KEY
            if assignee == "default": assignee = rest_create.JIRA_USER_NAME
        with allure.step("Send request"):
            r = rest_create.rest_jira_create_issue(summary, issue_type, project, description, assignee, priority)
        with allure.step("Check the status code"):
            assert r.status_code == status
