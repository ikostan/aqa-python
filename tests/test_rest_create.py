import pytest
import allure
from tests.rest.rest_issue_create import RestIssueCreate


@pytest.mark.rest
class TestRestLogin:

    @pytest.fixture(scope="module", autouse=True)
    def create(self, rest_set_session):
        cookie = rest_set_session
        return RestIssueCreate(cookie)

    @allure.title("REST JIRA. Create")
    @pytest.mark.parametrize("summary, description, issue_type, assignee_name, status_code", [
        ("Test Summary 1", "Test Summary 1 Description", "Bug", None, 201),
        ("Test Summary 2", "Test Summary 2 Description", "Bug", None, 201),
        ("Test Summary 3", "Test Summary 3 Description", "Bug", None, 201),
        ("Test Summary 4", "Test Summary 4 Description", "Bug", None, 201),
    ])
    def test_login(self, create, summary, description, issue_type, assignee_name, status_code):
        with allure.step("Send request"):
            r = create.rest_jira_create_issue(summary, description, issue_type, assignee_name)
        with allure.step("Check the status code"):
            assert r.status_code == status_code
