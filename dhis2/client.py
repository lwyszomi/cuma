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

    def get_users(self, fields):
        session = self.session
        response = session.get(self.url + 'users.json', params={'fields': fields})
        response_json = response.json()
        return response_json['users']

    def get_user(self, user_id):
        session = self.session
        fields = [
            ':all',
            'userCredentials[disabled]',
            'organisationUnits[displayName,level,ancestors[displayName,level]]',
            'userGroups[displayName]'
        ]
        response = session.get(self.url + 'users/%s.json' % user_id, params={
            'fields': ','.join(fields)
        })
        return response.json()
