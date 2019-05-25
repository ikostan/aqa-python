import json
import requests


class RestClient():
    JIRA_DOMAIN = 'https://jira.hillel.it'
    JIRA_SESSION = '/rest/auth/1/session'
    JIRA_ISSUE = '/rest/api/2/issue'
    JIRA_SEARCH = '/rest/api/2/search'
    JIRA_PROJECT_KEY = 'WEBINAR'

    def __init__(self):
        self.user_name = ''
        self.user_password = ''
        self.session_name = ''
        self.session_id = ''
        self.headers = {'Content-Type': 'application/json', 'Cookie': None}

    # REST REQUESTS
    def rest_jira_login(self, username, password):
        url = self.JIRA_DOMAIN + self.JIRA_SESSION
        payload = {"username": username, "password": password}
        headers = {'Content-Type': 'application/json'}
        return requests.post(url, json=payload, headers=headers)

    def rest_jira_create_issue(self, summary, description, issue_type="Bug", assignee_name=None):
        url = self.JIRA_DOMAIN + self.JIRA_ISSUE
        if assignee_name is not None: assignee_name = self.user_name
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
        return requests.post(url, data=payload, headers=self.headers)

    def rest_jira_search_all_my_issues(self):
        url = self.JIRA_DOMAIN + self.JIRA_SEARCH
        payload = self.dict_to_string(
            {
                "jql": "reporter = currentUser()",
                "startAt": 0,
                "maxResults": 1000,
                "fields": ["id"]
            }
        )
        return requests.post(url, data=payload, headers=self.headers)

    def rest_jira_delete_issue(self, issue_id):
        url = self.JIRA_DOMAIN + self.JIRA_ISSUE + '/' + issue_id
        payload = self.dict_to_string()
        return requests.delete(url, data=payload, headers=self.headers)

    # ACTIONS
    def dict_to_string(self, dict_value=None):
        got_string = ""
        if dict_value is not None and dict_value != "":
            got_string = json.dumps(dict_value)
        return got_string

    def set_session_with_login(self, username, password):
        self.user_name = username
        self.user_password = password
        response = self.rest_jira_login(self.user_name, self.user_password)
        if response.status_code == 200:
            got_json = response.json()
            self.session_name = got_json["session"]["name"]
            self.session_id = got_json["session"]["value"]
            self.headers['Cookie'] = self.session_name + "=" + self.session_id

    def set_session_without_login(self, username, password):
        self.user_name = username
        self.user_password = password

    def get_all_my_issues(self):
        search_result = self.rest_jira_search_all_my_issues()
        return search_result.json()["issues"]

    def get_all_my_issue_ids(self):
        id_list = []
        issue_objects = self.get_all_my_issues()
        if len(issue_objects) > 0:
            for issue in issue_objects:
                id_list.append(issue["id"])
        return id_list

    def delete_all_my_issues(self):
        id_list = self.get_all_my_issue_ids()
        if len(id_list) > 0:
            for id in id_list:
                self.rest_jira_delete_issue(id)
