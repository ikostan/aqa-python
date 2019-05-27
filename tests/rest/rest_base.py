import json
import requests
from tests.credentials import credentials


class RestBase:
    JIRA_DOMAIN = 'https://jira.hillel.it'
    JIRA_USER_NAME = credentials.user_login
    JIRA_USER_PASSWORD = credentials.user_login
    JIRA_PROJECT_KEY = credentials.project_key
    req = requests

    def __init__(self, cookie_value=None):
        self.session_name = ''
        self.session_id = ''
        self.headers = {'Content-Type': 'application/json', 'Cookie': cookie_value}

    def dict_to_string(self, dict_value=None):
        got_string = ""
        if dict_value is not None and dict_value != "":
            got_string = json.dumps(dict_value)
        return got_string
