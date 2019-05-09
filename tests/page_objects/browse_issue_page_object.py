from tests.page_objects.base_page_object import BasePageObject
from tests.page_objects.header_toolbar_fragment import HeaderToolbarFragment
from tests.page_objects.issue_details_fragment import IssueDetailsFragment


class BrowseIssuePageObject(BasePageObject):
    PAGE_URL_PART = "/browse/"

    def __init__(self, driver, url_optional=None):
        super().__init__(driver)
        self.header_toolbar = HeaderToolbarFragment(driver)
        self.issue_details = IssueDetailsFragment(driver)
        self.page_url_part = self.get_base_url() + self.PAGE_URL_PART
        self.page_url_part_with_project = self.page_url_part + self.get_project_key()
        self.page_url_full = url_optional

    def set_url_full_directly(self, url):
        self.page_url_full = url

    def set_url_full_directly_by_issue_id(self, issue_id):
        self.page_url_full = self.page_url_part_with_project + "-" + issue_id

    def get_url_full(self):
        return self.page_url_full

    def get_page_url_part(self):
        return self.page_url_part

    def get_page_url_part_with_project(self):
        return self.page_url_part_with_project

    def wait_until_page_is_opened(self, timeout=2):
        self.wait_until_url_contains(self.page_url_part_with_project, True, timeout)
        self.issue_details.wait_until_panel_is_opened(timeout)

    def open_page_by_url(self, url=None):
        if url is not None:
            self.page_url_full = url
        self.driver.get(self.page_url_full)
        self.wait_until_page_is_opened()
