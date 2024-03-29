import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject
from tests.rest.rest_session_login import RestSessionLogin


@pytest.fixture(scope="session")
def login_and_get_driver():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    login_page = LoginPageObject(driver)
    login_page.enter_site_as_test_user()
    yield driver


@pytest.fixture(scope="module")
def rest_set_session():
    login = RestSessionLogin()
    cookie = login.start_session()
    yield cookie


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    marker = item.get_closest_marker("ui")
    if marker:
        if rep.when == "call" and rep.failed:
            try:
                allure.attach(item.instance.driver.get_screenshot_as_png(), name=item.name,
                              attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(e)
