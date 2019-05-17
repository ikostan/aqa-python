import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject


class TestLogin:
    def setup_method(self):
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        self.login_page = LoginPageObject(self.driver)
        self.correct_login = self.login_page.get_user_login()
        self.correct_password = self.login_page.get_user_password()

    @pytest.mark.parametrize("login, password, result", [
        ("correct", "incorrect_password", False),
        ("incorrect_login", "correct", False),
        ("correct", "correct", True),
    ])
    def test_login_as_testing(self, login, password, result):
        if login == "correct":
            login = self.correct_login
        if password == "correct":
            password = self.correct_password
        got_result = self.login_page.login_user(login, password)
        self.driver.close()
        assert got_result == result
