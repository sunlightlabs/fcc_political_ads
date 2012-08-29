from django.utils import unittest
from django.core import mail
from django import test
from django.test.client import Client
from django.core.urlresolvers import reverse

from volunteers.forms import NonUserProfileForm


class NonUserProfileTestCase(test.TestCase):
    '''
        Tests for the 'non-user' profile.
    '''
    email = 'name@example.com'
    first_name = 'John'
    last_name = 'Doe'
    phone = '2125550000'
    state = 'NC'
    zipcode = 27514
    is_a = 'other'

    def setUp(self):
        self.valid_form_dict = {'email': self.email, 'first_name': self.first_name, 'last_name': self.last_name,
                    'phone': self.phone, 'state': self.state, 'zipcode': self.zipcode, 'is_a': self.is_a}
        self.valid_form = NonUserProfileForm(self.valid_form_dict)


    def test_form_is_invalid_without_email(self):
        '''NonUserProfileForm is invalid without email.'''
        form = NonUserProfileForm({'first_name': self.first_name, 'last_name': self.last_name,
                                    'phone': self.phone, 'state': self.state, 'zipcode': self.zipcode, 'is_a': self.is_a})
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_without_zipcode(self):
        '''NonUserProfileForm is invalid without email.'''
        form = NonUserProfileForm({'email': self.email, 'first_name': self.first_name, 'last_name': self.last_name,
                                    'phone': self.phone, 'state': self.state, 'is_a': self.is_a})
        self.assertFalse(form.is_valid())

    def test_nonuserprofileform_normal_post(self):
        '''NonUserProfileForm processes NonUserProfile entry, sends email message, and issues a redirect'''

        c = Client()
        response = c.post(reverse('noaccount_signup'), self.valid_form_dict)

        self.assertTrue(self.valid_form)

        self.assertNotEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response, '/')

    def test_nonuserprofileform_ajax_post(self):
        '''NonUserProfileForm processes NonUserProfile entry, sends email message, and issues a redirect'''

        c = Client()
        response = c.post(reverse('noaccount_signup'), self.valid_form_dict, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
