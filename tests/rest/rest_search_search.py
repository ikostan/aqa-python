from tests.rest.rest_search import RestSearch


class RestSearchSearch(RestSearch):

    def __init__(self, cookie_value):
        super().__init__(cookie_value)

    def rest_jira_search_issues(self, jql_string, max_result):
        url = self.JIRA_DOMAIN + self.JIRA_SEARCH
        payload = self.dict_to_string(self.__get_body(jql_string, max_result))
        return self.req.post(url, data=payload, headers=self.headers)

    def __get_body(self, jql_string, max_results):
        request_body = dict()
        request_body.update(self.__get_body_fields())
        request_body.update(self.__get_body_start_at())
        if jql_string is not None: request_body.update(self.__get_body_jql(jql_string))
        if max_results is not None: request_body.update(self.__get_body_max_results(max_results))
        return request_body

    def __get_body_fields(self):
        return dict(fields=["id"])

    def __get_body_start_at(self):
        return dict(startAt=0)

    def __get_body_jql(self, jql_string):
        return dict(jql=jql_string)

    def __get_body_max_results(self, max_results):
        return dict(maxResults=max_results)

    # actions
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
