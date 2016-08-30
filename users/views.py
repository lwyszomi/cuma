from django.http import JsonResponse
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View

import users.queries as queries
from collections import defaultdict


class UserListView(TemplateView):

    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        return super(UserListView, self).get_context_data(**kwargs)


class UserView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = request.POST
        length = int(post.get('length', 10))
        start = int(post.get('start', 10))
        page = start / length + 1
        users, total = queries.get_users(fields='id,displayName,userCredentials[username,disabled]', page_size=length, page=page)
        return JsonResponse(data={
          "draw": int(post.get('draw', 0)) + 1,
          "recordsTotal": total,
          "recordsFiltered": total,
          "data": [
              [
                  u['displayName'],
                  u['userCredentials']['username'],
                  'Inactive' if u['userCredentials']['disabled'] else 'Active',
                  reverse('show_user', kwargs={'user_id': u['id']})
              ] for u in users
          ]
        })


class ShowUserView(TemplateView):

    template_name = 'users/show_user.html'

    def get_context_data(self, **kwargs):
        user = queries.get_user(kwargs['user_id'])
        organizations = user['organisationUnits']
        org_dict = defaultdict(list)
        for org in organizations:
            country = None
            if org['ancestors']:
                country = org['ancestors'][0]

            if country:
                org_dict[country['displayName']].append(org['displayName'])
            else:
                org_dict[org['displayName']] = []

        kwargs['user'] = user
        kwargs['organizations'] = dict(org_dict)
        return super(ShowUserView, self).get_context_data(**kwargs)
