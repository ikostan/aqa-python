import pytest
import allure
from tests.rest.rest_issue_create import RestIssueCreate
from tests.rest.rest_issue_update import RestIssueUpdate
from tests.rest.rest_issue_get import RestIssueGet
from tests.rest.rest_issue_delete import RestIssueDelete


@pytest.mark.rest
class TestRestUpdate:
    original = {
        "summary": "Python AQA: Original Issue",
        "issue_type": "Bug",
        "assignee": "",
        "priority": "Medium"
    }

    updated = {
        "summary": "Python AQA: Updated Issue",
        "issue_type": "Task",
        "assignee": "default",
        "priority": "Lowest"
    }

    @pytest.fixture(scope="module", autouse=True)
    def rest_client(self, rest_set_session):
        cookie = rest_set_session
        create = RestIssueCreate(cookie)
        issue = create.create_issue(self.original["summary"], self.original["issue_type"], None, None,
                                    self.original["assignee"], self.original["priority"])
        yield {"update": RestIssueUpdate(cookie), "get": RestIssueGet(cookie), "issue": issue}
        rest_delete = RestIssueDelete(cookie)
        rest_delete.rest_jira_delete_issue(issue["id"])

    @allure.title("REST JIRA. Update")
    def test_update_issue(self, rest_client):
        with allure.step("Setup"):
            rest_update = rest_client["update"]
            rest_get = rest_client["get"]
            issue_id = rest_client["issue"]["id"]
            new_assignee = self.updated["assignee"]
            if new_assignee == "default": new_assignee = rest_update.JIRA_USER_NAME
        with allure.step("Send request"):
            r = rest_update.rest_jira_update_issue(issue_id, self.updated["summary"], self.updated["issue_type"], None,
                                                   new_assignee, self.updated["priority"])
        with allure.step("Check the status code"):
            assert r.status_code == 204
        with allure.step("Check the updated values"):
            issue = rest_get.get_issue(issue_id)
            assert issue["summary"] == self.updated["summary"]
            assert issue["issue_type"] == self.updated["issue_type"]
            assert issue["assignee"] == new_assignee
            assert issue["priority"] == self.updated["priority"]
