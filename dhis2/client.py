import requests


class DHIS2Client(object):

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    @property
    def session(self):
        session = requests.Session()
        session.auth = (self.username, self.password)
        return session

    def get_users(self):
        session = self.session
        response = session.get(self.url + 'users.json', params={'fields': 'displayName,name'})
        return response.json()['users']
