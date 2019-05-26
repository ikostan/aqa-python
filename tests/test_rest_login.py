import pytest
import allure
from tests.rest.rest_session_login import RestSessionLogin


@pytest.mark.rest
class TestRestLogin:

    @pytest.fixture(scope="module", autouse=True)
    def login(self):
        return RestSessionLogin()

    @allure.title("REST JIRA. Login")
    @pytest.mark.parametrize("username, password, status_code", [
        ("True", "True", 200),
        ("False", "True", 401),
        ("True", "False", 401),
        ("False", "False", 401),
    ])
    def test_login(self, login, username, password, status_code):
        with allure.step("Send request"):
            if username == "True": username = login.JIRA_USER_NAME
            if password == "True": password = login.JIRA_USER_PASSWORD
            r = login.rest_jira_login(username, password)
        with allure.step("Check the status code"):
            assert r.status_code == status_code
