import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject


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
