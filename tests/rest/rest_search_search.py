from tests.rest.rest_search import RestSearch


class RestSearchSearch(RestSearch):

    def __init__(self, cookie_value):
        super().__init__(cookie_value)

    def rest_jira_search_issues(self, jql, max_result):
        url = self.JIRA_DOMAIN + self.JIRA_SEARCH
        payload = self.dict_to_string(
            {
                "jql": jql,
                "startAt": 0,
                "maxResults": max_result,
                "fields": ["id"]
            }
        )
        return self.req.post(url, data=payload, headers=self.headers)

    def get_all_my_issues(self):
        jql = "reporter = currentUser()"
        max_result = 1000
        search_result = self.rest_jira_search_issues(jql, max_result)
        return search_result.json()["issues"]

    def get_all_my_issue_ids(self):
        id_list = []
        issue_objects = self.get_all_my_issues()
        if len(issue_objects) > 0:
            for issue in issue_objects:
                id_list.append(issue["id"])
        return id_list
