import pytest
import allure
from tests.rest.rest_issue_create import RestIssueCreate
from tests.rest.rest_search_search import RestSearchSearch
from tests.rest.rest_issue_delete import RestIssueDelete


@pytest.mark.rest
class TestRestSearch:
    list_of_issues = [
        ("PythonAQA: Issue For Searching 01", "Bug", None, "Description 01", None, "Medium"),
        ("PythonAQA: Issue For Searching 02", "Bug", None, None, None, "Medium"),
        ("PythonAQA: Issue For Searching 03", "Bug", None, "Description 03", None, "Medium"),
        ("PythonAQA: Issue For Searching 04", "Bug", None, "Description 04", None, None),
        ("PythonAQA: Issue For Searching 05", "Bug", None, "Description 05", None, "Medium"),
        ("PythonAQA: Issue For Searching 06", "Bug", None, "Description 06", None, "Medium"),
        ("PythonAQA: Issue For Searching 07", "Bug", None, "Description 07", None, "Medium"),
        ("PythonAQA: Issue For Searching 08", "Bug", None, "Description 08", None, "Medium"),
        ("PythonAQA: Issue For Searching 09", "Bug", None, "Description 09", None, "Medium"),
        ("PythonAQA: Issue For Searching 10", "Bug", None, "Description 10", None, "Medium"),
    ]

    @pytest.fixture(scope="module", autouse=True)
    def rest_client(self, rest_set_session):
        cookie = rest_set_session
        create = RestIssueCreate(cookie)
        created_issue_ids = create.create_issues(self.list_of_issues)
        yield RestSearchSearch(cookie)
        rest_delete = RestIssueDelete(cookie)
        rest_delete.delete_issues(created_issue_ids)


    @allure.title("REST JIRA. Search")
    @pytest.mark.parametrize("jql, results_number, status_code",
                             [
                                 ("text ~ 'PythonAQA: Issue For Searching 03'", 1, 200),
                                 ("text ~ 'PythonAQA: Issue For Searching'", 10, 200),
                                 ("text ~ 'SomeIncorrectValueThatNeverWillBeFound'", 0, 200),
                             ])
    def test_search_issue(self, rest_client, jql, results_number, status_code):
        with allure.step("Send request"):
            r = rest_client.rest_jira_search_issues(jql, results_number)
        with allure.step("Check the status code"):
            assert r.status_code == status_code
        with allure.step("Check the nuber of found issues"):
            assert len(r.json()["issues"]) == results_number
