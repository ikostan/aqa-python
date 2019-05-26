from tests.rest.rest_issue import RestIssue


class RestIssueCreate(RestIssue):

    def __init__(self, cookie_value):
        super().__init__(cookie_value)

    def rest_jira_create_issue(self, project_key, summary, issue_type_name, description, assignee_name, priority_name):
        url = self.JIRA_DOMAIN + self.JIRA_ISSUE
        payload = self.dict_to_string(
            self.__get_body(project_key, summary, issue_type_name, description, assignee_name, priority_name))
        return self.req.post(url, data=payload, headers=self.headers)

    def __get_body(self, project_key, summary, issue_type_name, description, assignee_name, priority_name):
        request_body = dict(fields={})
        if project_key is not None: request_body["fields"].update(self.__get_body_project(project_key))
        if summary is not None: request_body["fields"].update(self.__get_body_summary(summary))
        if issue_type_name is not None: request_body["fields"].update(self.__get_body_issue_type(issue_type_name))
        if description is not None: request_body["fields"].update(self.__get_body_description(description))
        if assignee_name is not None: request_body["fields"].update(self.__get_body_assignee(assignee_name))
        if priority_name is not None: request_body["fields"].update(self.__get_body_priority(priority_name))
        return request_body

    def __get_body_project(self, project_key):
        body_section = dict(project={})
        body_section["project"].update(dict(key=project_key))
        return body_section

    def __get_body_summary(self, summary):
        return dict(summary=summary)

    def __get_body_issue_type(self, issue_type_name):
        body_section = dict(issuetype={})
        body_section["issuetype"].update(dict(name=issue_type_name))
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
