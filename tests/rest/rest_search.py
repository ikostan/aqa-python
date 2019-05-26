from tests.rest.rest_base import RestBase


class RestSearch(RestBase):
    JIRA_SEARCH = '/rest/api/2/search'

    def __init__(self, cookie_value):
        super().__init__(cookie_value)
