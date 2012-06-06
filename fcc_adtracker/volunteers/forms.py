from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField, USStateField, USStateSelect
from django.contrib.localflavor.us import us_states


from registration.forms import RegistrationFormUniqueEmail

from .models import Profile, IS_A_CHOICES


class ProfileForm(forms.Form):
    phone = USPhoneNumberField(required=False)
    state = USStateField(widget=USStateSelect, help_text="Please select the state you will volunteer in.")
    is_a = forms.ChoiceField(required=False, choices=IS_A_CHOICES)


class UserFormExtra(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()

class RegistrationProfileUniqueEmail(RegistrationFormUniqueEmail, ProfileForm):
    pass