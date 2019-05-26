from tests.rest.rest_issue import RestIssue


class RestIssueGet(RestIssue):

    def __init__(self, cookie_value):
        super().__init__(cookie_value)

    def rest_jira_get_issue(self, issue_id_or_key):
        url = self.JIRA_DOMAIN + self.JIRA_ISSUE + "/" + issue_id_or_key
        payload = self.dict_to_string()
        return self.req.get(url, data=payload, headers=self.headers)

    # actions
    def get_issue(self, issue_id_or_key):
        r = self.rest_jira_get_issue(issue_id_or_key)
        return self.__get_issue(r.json()["fields"])

    def __get_issue(self, got_json):
        issue_object = dict()
        issue_object.update(self.__get_issue_summary(got_json))
        issue_object.update(self.__get_issue_type(got_json))
        issue_object.update(self.__get_issue_project(got_json))
        issue_object.update(self.__get_issue_description(got_json))
        issue_object.update(self.__get_issue_assignee(got_json))
        issue_object.update(self.__get_issue_priority(got_json))
        return issue_object

    def __get_issue_summary(self, got_json):
        return dict(summary=got_json["summary"])

    def __get_issue_type(self, got_json):
        return dict(issue_type=got_json["issuetype"]["name"])

    def __get_issue_project(self, got_json):
        return dict(project=got_json["project"]["key"])

    def __get_issue_description(self, got_json):
        return dict(description=got_json["description"])

    def __get_issue_assignee(self, got_json):
        assignee = None
        if got_json["assignee"] is not None: assignee = got_json["assignee"]["name"]
        return dict(assignee=assignee)

    def __get_issue_priority(self, got_json):
        return dict(priority=got_json["priority"]["name"])
