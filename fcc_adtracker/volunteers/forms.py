from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField, USStateField, USStateSelect
# from django.contrib.localflavor.us import us_states


from registration.forms import RegistrationFormUniqueEmail

from .models import Profile, IS_A_CHOICES


class ProfileForm(forms.Form):
    phone = USPhoneNumberField(required=False)
    state = USStateField(widget=USStateSelect, help_text="Please select the state you will volunteer in.")
    is_a = forms.ChoiceField(required=False, choices=IS_A_CHOICES, label='I am a:')


class RegistrationProfileUniqueEmail(RegistrationFormUniqueEmail, ProfileForm):
    pass


class SocialProfileForm(forms.Form):
    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    first_name = forms.CharField(required=False, max_length=64)
    last_name = forms.CharField(required=False, max_length=64)
    phone = USPhoneNumberField(required=False)
    state = USStateField(widget=USStateSelect, help_text="Please select the state you will volunteer in.")
    is_a = forms.ChoiceField(required=False, choices=IS_A_CHOICES, label='I am a:')

    def clean(self):

        cleaned_data = super(SocialProfileForm, self).clean()

        if 'username' in cleaned_data:
            username = cleaned_data['username']
            if User.objects.filter(username=username).exists():
                self._errors['username'] = self.error_class(["Username is already taken"])
                del cleaned_data['username']

        if 'email' in cleaned_data:
            email = cleaned_data['email']
            if User.objects.filter(email=email).exists():
                self._errors['email'] = self.error_class(["Email address has already been used"])
                del cleaned_data['email']

        return cleaned_data
