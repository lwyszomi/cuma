import requests

from django.conf import settings
from requests.exceptions import HTTPError


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

    def get_user_profile(self, username, password):
        response = requests.get(self.url + 'me.json', params={
            'fields': 'id,firstName,surname,email,userCredentials[username]'
        }, auth=(username, password))
        if response.status_code != 200:
            raise HTTPError(response=response)
        return response.json()

    def get_users(self):
        session = self.session
        fields = [
            'id',
            'displayName',
            'userCredentials[disabled,username,userRoles[displayName,id]]',
            'organisationUnits[displayName,level,id,ancestors[displayName,id,level]]',
            'userGroups[id,displayName]'
        ]
        response = session.get(self.url + 'users.json', params={
            'fields': ','.join(fields),
            'paging': 'false'
        })
        return response.json()['users']

    def get_user(self, user_id):
        session = self.session
        fields = [
            ':all',
            'userCredentials[disabled,username,userRoles[displayName,id]]',
            'organisationUnits[displayName,level,code,id,ancestors[displayName,level,code,id]]',
            'userGroups[displayName]',
        ]
        response = session.get(self.url + 'users/%s.json' % user_id, params={
            'fields': ','.join(fields)
        })
        return response.json()

    def get_organization_units(self):
        session = self.session
        max_level_response = session.get(self.url + 'organisationUnitLevels.json', params={'fields': 'level'})
        max_level = sorted([org['level'] for org in max_level_response.json()['organisationUnitLevels']])[-1]
        fields = 'children[displayName,code,id,level]'
        for _ in range(max_level, 0, -1):
            fields = 'children[displayName,code,id,level,%s]' % fields

        response = session.get(self.url + 'organisationUnits.json', params={
            'fields': 'displayName,code,id,level,%s' % fields,
            'paging': 'false',
            'filter': [
                'level:eq:%d' % settings.COUNTRY_LEVEL,
                'displayName:in:[Burma/Myanmar,Pakistan,Syria]' # TODO Remove this before deploy on production
            ]
        })

        return response.json()['organisationUnits']

    def get_countries(self):
        session = self.session
        countries = session.get(self.url + 'organisationUnits.json', params={
            'fields': 'id,level,displayName,code',
            'filter': 'level:eq:%d' % settings.COUNTRY_LEVEL,
            'paging': 'false'
        })
        return countries.json()['organisationUnits']

    def get_user_groups(self):
        session = self.session
        groups = session.get(self.url + 'userGroups.json', params={
            'fields': 'displayName,id',
            'paging': 'false'
        })
        return groups.json()['userGroups']

    def get_user_roles(self):
        session = self.session
        groups = session.get(self.url + 'userRoles.json', params={
            'fields': 'displayName,id',
            'paging': 'false'
        })
        return groups.json()['userRoles']

    def get_role_by_name(self, role_name):
        session = self.session
        groups = session.get(self.url + 'userRoles.json', params={
            'fields': 'displayName,id',
            'filter': 'displayName:eq:%s' % role_name,
            'paging': 'false'
        })
        return groups.json()['userRoles']
