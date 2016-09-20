from django.core.management.base import BaseCommand
import users.queries as queries

class Command(BaseCommand):

    def handle(self, *args, **options):
        role = queries.get_dashboard_role()[0]
        users = queries.get_users_without_role(role['id'])

        for user in users:
            user['userCredentials']['userRoles'].append(role)
            response = queries.save_user(user)

            if response.status_code == 200:
                print 'User was succesfully updated'
            else:
                print 'Error updating user, reason:\n' + response.reason



