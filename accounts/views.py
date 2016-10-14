from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from accounts.forms import DHISAuthForm

from django.conf import settings

from accounts.models import CometServerConfiguration
from dhis2.auth import DHIS2AuthenticationException


class LoginView(TemplateView):
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return redirect('users')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = kwargs.get('form') or DHISAuthForm()
        kwargs['dhis2_url'] = CometServerConfiguration.objects.first().url
        return super(LoginView, self).get_context_data(**kwargs)

    def post(self, request, **kwargs):
        form = DHISAuthForm(request.POST)
        if not form.is_valid():
            kwargs['form'] = form
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

        cleaned_data = form.clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        try:
            user = authenticate(
                username=username,
                password=password,
                session=request.session,
            )
            if user:
                if user.is_active:
                    login(request, user)
                    next = request.GET.get('next', reverse('home'))
                    return redirect(next)
                else:
                    messages.error(request, 'User inactive.', 'danger')
            else:
                messages.error(request, 'Invalid login credentials.', 'danger')
        except DHIS2AuthenticationException as e:
            messages.error(request, e.message, 'danger')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


def logout_view(request):
    if not request.user.username:
        return redirect('accounts:login')

    logout(request)
    comet_configuration_server = CometServerConfiguration.objects.first()
    return redirect(comet_configuration_server.url)


def comet_entry_view(request):
    url = reverse('accounts:login')
    logout(request)
    return redirect(url)
