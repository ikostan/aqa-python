from tests.rest.rest_session import RestSession


class RestSessionLogin(RestSession):

    def __init__(self):
        super().__init__()

    def rest_jira_login(self, username, password):
        url = self.JIRA_DOMAIN + self.JIRA_SESSION
        payload = {"username": username, "password": password}
        headers = {'Content-Type': 'application/json'}
        return self.req.post(url, json=payload, headers=headers)

    def start_session(self):
        response = self.rest_jira_login(self.JIRA_USER_NAME, self.JIRA_USER_PASSWORD)
        if response.status_code == 200:
            got_json = response.json()
            return got_json["session"]["name"] + "=" + got_json["session"]["value"]
