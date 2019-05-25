import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject
from tests.rest.rest_client import RestClient
from tests.credentials import credentials


@pytest.fixture(scope="module")
def login_and_get_driver():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    login_page = LoginPageObject(driver)
    login_page.enter_site_as_test_user()
    yield driver
    try:
        driver.close()
        # driver.quit()
    except:
        pass


@pytest.fixture(scope="module")
def rest_set_session_with_login():
    rest = RestClient()
    user = get_user_creds()
    rest.set_session_with_login(user['login'], user['pass'])
    yield rest
    rest.delete_all_my_issues()


@pytest.fixture(scope="module")
def rest_set_session_without_login():
    rest = RestClient()
    user = get_user_creds()
    rest.set_session_without_login(user['login'], user['pass'])
    yield rest


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    marker = item.get_closest_marker("ui")
    if marker:
        if rep.when == "call" and rep.failed:
            try:
                allure.attach(item.instance.driver.get_screenshot_as_png(),
                              name=item.name,
                              attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(e)


def get_user_creds():
    return {'login': credentials.user_login, 'pass': credentials.user_password}
