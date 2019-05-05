from selenium.webdriver.common.by import By
from tests.page_objects.base_page_object import BasePageObject


class CreateIssueModal(BasePageObject):
    MODAL = (By.ID, "create-issue-dialog")
    SPINNER = (By.CSS_SELECTOR, ".throbber.loading aui-spinner")
    PROJECT_COMBOBOX = (By.ID, "project-single-select")
    ISSUE_TYPE_COMBOBOX = (By.ID, "issuetype-single-select")
    ISSUE_SUMMARY = (By.ID, "summary")
    ISSUE_DESCRIPTION_FRAME = (By.CSS_SELECTOR, " .mce-edit-area iframe")
    ISSUE_DESCRIPTION_BODY = (By.CSS_SELECTOR, " .mce-content-body")
    PRIORITY_COMBOBOX = (By.ID, "priority-single-select")
    CREATE_BUTTON = (By.ID, "create-issue-submit")

    def __init__(self, driver):
        super().__init__(driver)

    # waits
    def wait_until_modal_is_opened(self, timeout=3):
        self.wait_until_element_is_present(self.MODAL, timeout)

    def wait_until_modal_is_not_opened(self, timeout=3):
        self.wait_until_element_is_not_present(self.MODAL, timeout)

    def wait_until_spinner_is_disappeared(self, timeout=2):
        self.wait_until_element_is_present(self.SPINNER, timeout)

    def wait_until_create_button_is_clickable(self, timeout=2):
        self.wait_until_element_is_clickable(self.CREATE_BUTTON, timeout)

    def wait_until_data_is_stored(self):
        self.wait_until_spinner_is_disappeared()
        self.wait_until_create_button_is_clickable()

    # select in combobox
    def select_project(self, project_name=None):
        if project_name is not None:
            self.pick_in_combobox(self.PROJECT_COMBOBOX, project_name)
            self.wait_until_data_is_stored()

    def select_issue_type(self, issue_type_name=None):
        if issue_type_name is not None:
            self.pick_in_combobox(self.ISSUE_TYPE_COMBOBOX, issue_type_name)
            self.wait_until_data_is_stored()

    def select_priority(self, priority_name=None):
        if priority_name is not None:
            self.pick_in_combobox(self.PRIORITY_COMBOBOX, priority_name)
            self.wait_until_data_is_stored()

    # populate text
    def populate_summary(self, summary_content=None):
        if summary_content is not None:
            element = self.driver.find_element(*self.ISSUE_SUMMARY)
            element.clear()
            element.send_keys(summary_content)
            self.wait_until_data_is_stored()

    def populate_description(self, description_content=None):
        if description_content is not None:
            editor_frame = self.driver.find_element(*self.ISSUE_DESCRIPTION_FRAME)
            self.driver.switch_to.frame(editor_frame)
            description_body = self.driver.find_element(*self.ISSUE_DESCRIPTION_BODY)
            description_body.clear()
            description_body.send_keys(description_content)
            self.driver.switch_to.default_content()
            self.wait_until_data_is_stored()

    # clicks
    def click_create_button(self):
        self.driver.find_element(*self.CREATE_BUTTON).click()

    # complex actions
    def populate_fields_and_click_create(self, project, issue_type, summary, description, priority):
        self.select_project(project)
        self.select_issue_type(issue_type)
        self.populate_summary(summary)
        self.populate_description(description)
        self.select_priority(priority)
        self.click_create_button()
