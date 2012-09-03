from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from passwords.fields import PasswordField

PASSWORD_HELP_TEXT = getattr(settings, 'PASSWORD_HELP_TEXT', u'Please choose a strong password.')


class HelpfulPasswordField(PasswordField):
    def __init__(self, required=True, widget=None, label=None, initial=None,
                 help_text=None, error_messages=None, show_hidden_initial=False,
                 validators=[], localize=False):
        super(HelpfulPasswordField, self).__init__(required=True, widget=None, label=None, initial=None,
                 help_text=None, error_messages=None, show_hidden_initial=False,
                 validators=[], localize=False)
        self.help_text = PASSWORD_HELP_TEXT


class TougherSetPasswordForm(SetPasswordForm):
    new_password1 = HelpfulPasswordField(label=_("New password"))
    new_password2 = HelpfulPasswordField(label=_("New password confirmation"))


class TougherChangePasswordForm(PasswordChangeForm, TougherSetPasswordForm):
    new_password1 = HelpfulPasswordField(label=_("New password"))
