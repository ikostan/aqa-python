from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.page_objects.base_page_object import BasePageObject
from tests.page_objects.flag_container_page_object import FlagContainerPageObject


class IssueDetailsFragment(BasePageObject):
    PROJECT_AVATAR_ELEMENT = (By.ID, "project-avatar")
    PROJECT_NAME_ELEMENT = (By.ID, "project-name-val")
    ISSUE_KEY_ID_ELEMENT = (By.ID, "key-val")
    ISSUE_SUMMARY = (By.ID, "summary-val")
    ISSUE_SUMMARY_INPUT = (By.ID, "summary")
    ISSUE_SUMMARY_SPINNER = (By.CSS_SELECTOR, "#summary-val .throbber")
    ISSUE_SUMMARY_ERROR = (By.CSS_SELECTOR, " .error.inline-edit-error")
    ISSUE_SUMMARY_CANCEL = (By.CSS_SELECTOR, "#summary-val .aui-button.cancel")
    ISSUE_PRIORITY = (By.ID, "priority-val")
    ISSUE_PRIORITY_FORM = (By.ID, "priority-form")
    ISSUE_PRIORITY_SPINNER = (By.CSS_SELECTOR, "#priority-form .throbber")
    ISSUE_ASSIGNEE = (By.ID, "assignee-val")
    ISSUE_ASSIGNEE_FORM = (By.ID, "assignee-single-select")
    ISSUE_ASSIGNEE_SPINNER = (By.CSS_SELECTOR, "#assignee-form .throbber")
    MORE_BUTTON = (By.ID, "opsbar-operations_more")
    MORE_DROP = (By.ID, "opsbar-operations_more_drop")
    MORE_DROP_DELETE_ISSUE_ITEM = (By.ID, "delete-issue")
    DELETE_ISSUE_DIALOG = (By.ID, "delete-issue-dialog")
    DELETE_ISSUE_DIALOG_SUBMIT = (By.ID, "delete-issue-submit")
    DELETE_ISSUE_DIALOG_CANCEL = (By.ID, "delete-issue-cancel")

    def __init__(self, driver):
        super().__init__(driver)
        self.flag = FlagContainerPageObject(driver)

    def get_issue_key_id(self):
        return self.driver.find_element(*self.ISSUE_KEY_ID_ELEMENT).text

    def get_issue_summary(self):
        return self.driver.find_element(*self.ISSUE_SUMMARY).text

    def get_issue_summary_error(self):
        try:
            return self.driver.find_element(*self.ISSUE_SUMMARY_ERROR).text
        except:
            return None

    def get_issue_priority(self):
        return self.driver.find_element(*self.ISSUE_PRIORITY).text

    def get_issue_assignee(self):
        return self.driver.find_element(*self.ISSUE_ASSIGNEE).text

    def wait_until_panel_is_opened(self, timeout=2):
        return self.wait_until_element_is_present(self.PROJECT_NAME_ELEMENT, True, timeout)

    def wait_for_dropdown(self, dropdown_locator, true_false_to_open_close=True):
        if true_false_to_open_close:
            self.wait_until_element_is_visible(dropdown_locator, True)
        else:
            self.wait_until_element_is_visible(dropdown_locator, False)

    def click_more_button(self):
        self.wait_until_element_is_present(self.MORE_BUTTON, True, 4)
        self.driver.find_element(*self.MORE_BUTTON).click()

    def click_more_drop_delete_issue_item(self):
        self.wait_until_element_is_present(self.MORE_DROP_DELETE_ISSUE_ITEM, True, 2)
        self.driver.find_element(*self.MORE_DROP_DELETE_ISSUE_ITEM).click()

    def click_summary_element(self):
        self.driver.find_element(*self.ISSUE_SUMMARY).click()
        self.wait_until_element_is_present(self.ISSUE_SUMMARY_INPUT, True)

    def click_summary_cancel(self):
        self.wait_until_element_is_present(self.ISSUE_SUMMARY_CANCEL, True, 2)
        self.driver.find_element(*self.ISSUE_SUMMARY_CANCEL).click()

    def click_priority_element(self):
        self.driver.find_element(*self.ISSUE_PRIORITY).click()
        self.wait_until_element_is_present(self.ISSUE_PRIORITY_FORM, True, 2)

    def click_assignee_element(self):
        self.driver.find_element(*self.ISSUE_ASSIGNEE).click()
        self.wait_until_element_is_present(self.ISSUE_ASSIGNEE_FORM, True, 2)

    def update_summary(self, summary_name=None, true_if_allow_empty_input=False):
        if summary_name is not None:
            if summary_name != "" or true_if_allow_empty_input:
                self.click_summary_element()
                summary_input = self.driver.find_element(*self.ISSUE_SUMMARY_INPUT)
                summary_input.clear()
                summary_input.send_keys(summary_name)
                summary_input.send_keys(Keys.ENTER)
                if summary_name != "" and len(summary_name) < 256:
                    self.wait_until_element_is_present(self.ISSUE_SUMMARY_SPINNER, False)

    def select_priority(self, priority_name=None):
        if priority_name is not None and priority_name != "":
            self.click_priority_element()
            self.pick_in_combobox(self.ISSUE_PRIORITY_FORM, priority_name, True)
            self.wait_until_element_is_present(self.ISSUE_PRIORITY_SPINNER, False)

    def select_assignee(self, assignee_name=None):
        if assignee_name is not None and assignee_name != "":
            self.click_assignee_element()
            self.pick_in_combobox(self.ISSUE_ASSIGNEE_FORM, assignee_name, True)
            self.wait_until_element_is_present(self.ISSUE_ASSIGNEE_SPINNER, False)

    def delete_issue(self):
        self.click_more_button()
        self.wait_for_dropdown(self.MORE_DROP, True)
        self.click_more_drop_delete_issue_item()
        self.wait_for_dropdown(self.MORE_DROP, False)
        self.wait_until_element_is_present(self.DELETE_ISSUE_DIALOG, True, 2)
        self.driver.find_element(*self.DELETE_ISSUE_DIALOG_SUBMIT).click()
        self.flag.wait_until_flag_is_shown()
