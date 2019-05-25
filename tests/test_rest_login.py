import pytest
import allure


@pytest.mark.rest
class TestRestLogin:
    created_issues = []

    @pytest.fixture(scope="module", autouse=True)
    def rest(self, rest_set_session_without_login):
        return rest_set_session_without_login

    @allure.title("REST JIRA. Login")
    @pytest.mark.parametrize("login, password, status_code", [
        ("True", "True", 200),
        ("False", "True", 401),
        ("True", "False", 401),
        ("False", "False", 401),
    ])
    def test_login(self, rest, login, password, status_code):
        # "Send request where the login is " + login + " and password is " + password
        with allure.step("Send request"):
            if login == "True": login = rest.user_name
            if password == "True": password = rest.user_password
            r = rest.rest_jira_login(login, password)
        # "Check the status code is " + status_code
        with allure.step("Check the status code"):
            assert r.status_code == status_code
