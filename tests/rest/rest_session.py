from tests.rest.rest_base import RestBase


class RestSession(RestBase):
    JIRA_SESSION = '/rest/auth/1/session'

    def __init__(self, cookie_value=None):
        super().__init__(cookie_value)
