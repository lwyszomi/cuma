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
        fields = [
            'id',
            'displayName',
            'userCredentials[disabled,username]'
        ]
        response = session.get(self.url + 'users.json', params={'fields': ','.join(fields)})
        return response.json()['users']


    def get_user(self, user_id):
        session = self.session
        fields = [
            ':all',
            'userCredentials[disabled,username]',
            'organisationUnits[displayName,level,ancestors[displayName,level]]',
            'userGroups[displayName]'
        ]
        response = session.get(self.url + 'users/%s.json' % user_id, params={
            'fields': ','.join(fields)
        })
        return response.json()

    def get_organization_units(self):
        session = self.session
        max_level_response = session.get(self.url + 'filledOrganisationUnitLevels.json')
        max_level = max_level_response.json()[-1]['level']
        fields = 'children[displayName,id]'
        while max_level > 0:
            fields = 'children[displayName,id,%s]' % fields
            max_level -= 1

        response = session.get(self.url + 'organisationUnits.json', params={
            'fields': 'displayName,id,%s' % fields,
            'filter': 'level:eq:3'
        })

        return response.json()['organisationUnits']
