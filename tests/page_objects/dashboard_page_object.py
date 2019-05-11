from tests.page_objects.base_page_object import BasePageObject
from tests.page_objects.fragments.header_toolbar_fragment import HeaderToolbarFragment
from tests.page_objects.flag_container_page_object import FlagContainerPageObject


class DashboardPageObject(BasePageObject):
    PAGE_URL_PART = "/secure/Dashboard.jspa"

    def __init__(self, driver):
        super().__init__(driver)
        self.header_toolbar = HeaderToolbarFragment(driver)
        self.flag = FlagContainerPageObject(driver)

    def get_url(self):
        return self.get_base_url() + self.PAGE_URL_PART

    def wait_until_page_is_opened(self):
        return self.header_toolbar.wait_until_user_button_is_present()

    def open_page(self):
        page_url = self.get_url()
        self.driver.get(page_url)
        self.wait_until_page_is_opened()
