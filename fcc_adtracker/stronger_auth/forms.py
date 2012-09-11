from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms.widgets import PasswordInput

from passwords.fields import PasswordField

PASSWORD_HELP_TEXT = getattr(settings, 'PASSWORD_HELP_TEXT', u'Please choose a strong password.')
PASSWORD_CONFIRM_HELP_TEXT = getattr(settings, 'PASSWORD_CONFIRM_HELP_TEXT', u'Please confirm your new password.')


class TougherSetPasswordForm(SetPasswordForm):
    new_password1 = PasswordField(label=_("New password"), help_text=PASSWORD_HELP_TEXT)
    new_password2 = PasswordField(label=_("New password confirmation"), help_text=PASSWORD_HELP_TEXT)


class TougherChangePasswordForm(PasswordChangeForm, TougherSetPasswordForm):
    new_password1 = PasswordField(label=_("New password"), help_text=PASSWORD_HELP_TEXT)
