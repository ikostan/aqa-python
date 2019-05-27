from tests.rest.rest_base import RestBase


class RestIssue(RestBase):
    JIRA_ISSUE = '/rest/api/2/issue'

    def __init__(self, cookie_value):
        super().__init__(cookie_value)
