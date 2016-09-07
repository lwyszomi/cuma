from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from django.conf import settings


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.username in getattr(settings, 'SUPERUSER_LIST', ('admin',)):
            return redirect('admin:index')
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
