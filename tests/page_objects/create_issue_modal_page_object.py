from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject


class CreateIssueModal(BasePageObject):
    MODAL = (By.ID, "create-issue-dialog")
    SPINNER = (By.CSS_SELECTOR, ".throbber.loading aui-spinner")
    PROJECT_COMBOBOX = (By.ID, "project-single-select")
    ISSUE_TYPE_COMBOBOX = (By.ID, "issuetype-single-select")
    ISSUE_SUMMARY = (By.ID, "summary")
    ISSUE_SUMMARY_ERROR = (By.CSS_SELECTOR, " .error[data-field='summary']")
    ISSUE_DESCRIPTION_FRAME = (By.CSS_SELECTOR, " .mce-edit-area iframe")
    ISSUE_DESCRIPTION_BODY = (By.CSS_SELECTOR, " .mce-content-body")
    PRIORITY_COMBOBOX = (By.ID, "priority-single-select")
    CREATE_BUTTON = (By.ID, "create-issue-submit")
    CANCEL_BUTTON = (By.CSS_SELECTOR, " .jira-dialog a.cancel")

    def __init__(self, driver):
        super().__init__(driver)

    # waits
    def wait_until_modal_is_opened(self, timeout=3):
        return self.wait_until_element_is_present(self.MODAL, True, timeout)

    def wait_until_modal_is_not_opened(self, timeout=3):
        return self.wait_until_element_is_present(self.MODAL, False, timeout)

    def wait_until_spinner_is_disappeared(self, timeout=5):
        return self.wait_until_element_is_present(self.SPINNER, False, timeout)

    def wait_until_create_button_is_clickable(self, timeout=2):
        return self.wait_until_element_is_clickable(self.CREATE_BUTTON, True, timeout)

    def wait_until_summary_error_is_existing(self, timeout=2):
        return self.wait_until_element_is_present(self.ISSUE_SUMMARY_ERROR, True, timeout)

    def wait_until_data_is_stored(self):
        self.wait_until_spinner_is_disappeared()
        self.wait_until_create_button_is_clickable()

    # states
    def is_modal_existing(self):
        return self.is_element_displayed(self.MODAL)

    # gets
    def get_issue_summary_error_message(self, timeout=2):
        message = None
        if self.wait_until_summary_error_is_existing(timeout):
            message = self.driver.find_element(*self.ISSUE_SUMMARY_ERROR).text
        return message

    # select in combobox
    def select_project(self, project_name=None):
        if project_name is not None and project_name != "":
            self.pick_in_combobox(self.PROJECT_COMBOBOX, project_name)
            self.wait_until_data_is_stored()

    def select_issue_type(self, issue_type_name=None):
        if issue_type_name is not None and issue_type_name != "":
            self.pick_in_combobox(self.ISSUE_TYPE_COMBOBOX, issue_type_name)
            self.wait_until_data_is_stored()

    def select_priority(self, priority_name=None):
        if priority_name is not None and priority_name != "":
            self.pick_in_combobox(self.PRIORITY_COMBOBOX, priority_name)
            self.wait_until_data_is_stored()

    # populate text
    def populate_summary(self, summary_content=None):
        if summary_content is not None and summary_content != "":
            element = self.driver.find_element(*self.ISSUE_SUMMARY)
            self.wait_until_element_is_clickable(self.ISSUE_SUMMARY, True)
            interact_result = False
            i = 0
            while i < 5 and interact_result is not True:
                try:
                    element.clear()
                    element.send_keys(summary_content)
                    interact_result = True
                except Exception as e:
                    print(e)
                    interact_result = False
                i += 1
            self.wait_until_data_is_stored()

    def populate_description(self, description_content=None):
        if description_content is not None and description_content != "":
            editor_frame = self.driver.find_element(*self.ISSUE_DESCRIPTION_FRAME)
            self.driver.switch_to.frame(editor_frame)
            description_body = self.driver.find_element(*self.ISSUE_DESCRIPTION_BODY)
            description_body.clear()
            description_body.send_keys(description_content)
            self.driver.switch_to.default_content()
            self.wait_until_data_is_stored()

    # clicks
    def click_create_button(self):
        self.wait_until_data_is_stored()
        self.driver.find_element(*self.CREATE_BUTTON).click()

    def click_cancel_button(self):
        self.wait_until_data_is_stored()
        self.driver.find_element(*self.CANCEL_BUTTON).click()

    # complex actions
    def populate_fields_and_click_create(self, project, issue_type, summary, description, priority):
        self.select_project(project)
        self.select_issue_type(issue_type)
        self.populate_summary(summary)
        self.populate_description(description)
        self.select_priority(priority)
        self.click_create_button()

    def cancel_creation(self):
        self.click_cancel_button()
        self.alert_wait_and_confirm()
        self.wait_until_modal_is_not_opened()
