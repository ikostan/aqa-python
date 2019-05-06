from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject
from tests.page_objects.flag_container_page_object import FlagContainerPageObject


class IssueDetailsFragment(BasePageObject):
    PROJECT_AVATAR_ELEMENT = (By.ID, "project-avatar")
    PROJECT_NAME_ELEMENT = (By.ID, "project-name-val")
    ISSUE_KEY_ID_ELEMENT = (By.ID, "key-val")
    MORE_BUTTON = (By.ID, "opsbar-operations_more")
    MORE_DELETE_ISSUE_ITEM = (By.ID, "delete-issue")
    DELETE_ISSUE_DIALOG = (By.ID, "delete-issue-dialog")
    DELETE_ISSUE_DIALOG_SUBMIT = (By.ID, "delete-issue-submit")
    DELETE_ISSUE_DIALOG_CANCEL = (By.ID, "delete-issue-cancel")

    def __init__(self, driver):
        super().__init__(driver)
        self.flag = FlagContainerPageObject(driver)

    def get_issue_key_id(self):
        return self.driver.find_element(*self.ISSUE_KEY_ID_ELEMENT).text

    def wait_until_panel_is_opened(self):
        return self.wait_until_element_is_present(self.PROJECT_NAME_ELEMENT)

    def wait_for_dropdown(self, clicked_button, true_false_to_open_close=True):
        if true_false_to_open_close:
            self.wait_until_attribute_value_is(clicked_button, "aria-expanded", "true")
        else:
            self.wait_until_attribute_value_is(clicked_button, "aria-expanded", "false")

    def click_more_button(self):
        self.driver.find_element(*self.MORE_BUTTON).click()

    def click_more_delete_issue_item(self):
        self.driver.find_element(*self.MORE_DELETE_ISSUE_ITEM).click()

    def delete_issue(self):
        self.click_more_button()
        self.wait_for_dropdown(self.MORE_BUTTON, True)
        self.click_more_delete_issue_item()
        self.wait_for_dropdown(self.MORE_BUTTON, False)
        self.wait_until_element_is_present(self.DELETE_ISSUE_DIALOG, 2)
        self.driver.find_element(*self.DELETE_ISSUE_DIALOG_SUBMIT).click()
        self.flag.wait_until_flag_is_shown()
