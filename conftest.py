import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tests.page_objects.login_page_object import LoginPageObject


@pytest.fixture
def login_and_get_driver():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.fullscreen_window()
    login_page = LoginPageObject(driver)
    login_page.enter_site_as_test_user()
    return driver
