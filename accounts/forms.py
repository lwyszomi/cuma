from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from django import forms


class DHISAuthForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Please sign in',
                Field('username', css_class='input-lg'),
                Field('password', css_class='input-lg'),
                Field('server', css_class='input-lg')
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-lg btn-primary btn-block')
            )
        )
        self.helper.form_class = 'form-signin'
        self.helper.form_action = '.'
        super(DHISAuthForm, self).__init__(*args, **kwargs)
