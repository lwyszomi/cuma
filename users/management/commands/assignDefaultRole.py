from django.core.management.base import BaseCommand
from dhis2.utils import get_client
from django.http import JsonResponse
from django.urls.base import reverse
import users.queries as queries

class Command(BaseCommand):

    def handle(self, *args, **options):
        client = get_client()

        role = queries.get_dashboard_role()[0]
        users = queries.get_users_without_role(role['id'])

        for user in users:
            user['userCredentials']['userRoles'].append(role)

            #caly user
            #user = queries.get_user(user['id'])
            #user['userCredentials']['userRoles'].append(role)
            response = queries.update_user(user)

            if response.status_code == 200:
                return JsonResponse(data={'redirect': reverse('show_user', kwargs={'user_id': user['id']})})
            else:
                return JsonResponse(data={'error': 'Error'})



