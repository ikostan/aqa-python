from tests.rest.rest_issue import RestIssue


class RestIssueCreate(RestIssue):

    def __init__(self, cookie_value):
        super().__init__(cookie_value)

    def rest_jira_create_issue(self, summary, description, issue_type="Bug", assignee_name=None):
        url = self.JIRA_DOMAIN + self.JIRA_ISSUE
        if assignee_name is None: assignee_name = self.JIRA_USER_NAME
        payload = self.dict_to_string(
            {
                "fields": {
                    "project": {
                        "key": self.JIRA_PROJECT_KEY
                    },
                    "summary": summary,
                    "description": description,
                    "issuetype": {
                        "name": issue_type
                    },
                    "assignee": {
                        "name": assignee_name
                    }
                }
            }
        )
        return self.req.post(url, data=payload, headers=self.headers)
