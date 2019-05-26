from tests.rest.rest_issue import RestIssue


class RestIssueCreate(RestIssue):

    def __init__(self, cookie_value):
        super().__init__(cookie_value)

    def rest_jira_create_issue(self, summary, issue_type_name, project_key, description, assignee_name, priority_name):
        url = self.JIRA_DOMAIN + self.JIRA_ISSUE
        payload = self.dict_to_string(
            self.__get_body(summary, issue_type_name, project_key, description, assignee_name, priority_name))
        return self.req.post(url, data=payload, headers=self.headers)

    def __get_body(self, summary, issue_type_name, project_key, description, assignee_name, priority_name):
        request_body = dict(fields={})
        if summary is not None: request_body["fields"].update(self.__get_body_summary(summary))
        if issue_type_name is not None: request_body["fields"].update(self.__get_body_issue_type(issue_type_name))
        if project_key is not None: request_body["fields"].update(self.__get_body_project(project_key))
        if description is not None: request_body["fields"].update(self.__get_body_description(description))
        if assignee_name is not None: request_body["fields"].update(self.__get_body_assignee(assignee_name))
        if priority_name is not None: request_body["fields"].update(self.__get_body_priority(priority_name))
        return request_body

    def __get_body_summary(self, summary):
        return dict(summary=summary)

    def __get_body_issue_type(self, issue_type_name):
        body_section = dict(issuetype={})
        body_section["issuetype"].update(dict(name=issue_type_name))
        return body_section

    def __get_body_project(self, project_key):
        body_section = dict(project={})
        body_section["project"].update(dict(key=project_key))
        return body_section

    def __get_body_description(self, description):
        return dict(description=description)

    def __get_body_assignee(self, assignee_name):
        body_section = dict(assignee={})
        body_section["assignee"].update(dict(name=assignee_name))
        return body_section

    def __get_body_priority(self, priority_name):
        body_section = dict(priority={})
        body_section["priority"].update(dict(name=priority_name))
        return body_section

    # actions
    def create_issue(self, summary, issue_type_name, project_key=None, description=None, assignee_name=None,
                     priority_name=None):
        if project_key is None or project_key == "": project_key = self.JIRA_PROJECT_KEY
        return self.rest_jira_create_issue(summary, issue_type_name, project_key, description, assignee_name,
                                           priority_name)

    def create_issues(self, list_of_tuples):
        if len(list_of_tuples) > 0:
            for one_tuple in list_of_tuples:
                self.create_issue(one_tuple[0], one_tuple[1], one_tuple[2], one_tuple[3], one_tuple[4], one_tuple[5])
