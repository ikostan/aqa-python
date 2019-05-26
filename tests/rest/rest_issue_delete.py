from tests.rest.rest_issue import RestIssue


class RestIssueDelete(RestIssue):

    def __init__(self, cookie_value):
        super().__init__(cookie_value)

    def rest_jira_delete_issue(self, issue_id):
        url = self.JIRA_DOMAIN + self.JIRA_ISSUE + '/' + issue_id
        payload = self.dict_to_string()
        return self.req.delete(url, data=payload, headers=self.headers)

    def delete_issues(self, id_list):
        if len(id_list) > 0:
            for id in id_list:
                self.rest_jira_delete_issue(id)
