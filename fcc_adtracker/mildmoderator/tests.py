from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, AnonymousUser
from fccpublicfiles.models import Person
from broadcasters.models import Broadcaster
from mock import patch

import os.path
import unittest2


class BaseModerationTest(TestCase):
    def setUp(self):
        self.volunteer_user = self.create_user_with_name_for_group('jack', 'Volunteers')
        self.professional_user = self.create_user_with_name_for_group('jill', 'Professionals')
        self.superuser = self.create_superuser()

    def create_user_with_name_for_group(self, username, group_name):
        user = User.objects.create(username=username)
        user.set_password('abc123')
        user.save()
        group = Group.objects.create(name=group_name)
        user.groups.add(group)

        return user

    def create_superuser(self):
        superuser = User.objects.create(username='janice', is_superuser=True)
        superuser.set_password('abc123')
        superuser.save()

        return superuser


class ModelSaveTest(BaseModerationTest):

    def test_save_person_populates_created_by(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        self.assertEqual(person.created_by, self.volunteer_user)

    def test_save_person_does_not_initially_populate_updated_by(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        self.assertIsNone(person.updated_by)

    def test_update_person_populates_updated_by(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        person.middle_name = 'Ignatius'

        person.save(self.volunteer_user)

        self.assertEqual(person.updated_by, self.volunteer_user)

    def test_update_is_public_to_true_populates_approved_by__for_users_in_right_group(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.professional_user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(self.professional_user)

        self.assertEqual(person.approved_by, self.professional_user)

    def test_update_is_public_to_true_populates_approved_by__for_superusers(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.superuser)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(self.superuser)

        self.assertEqual(person.approved_by, self.superuser)

    def test_update_is_public_to_true_doesnt_populate_approved_by__for_users_in_wrong_group(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(self.volunteer_user)

        self.assertIsNone(person.approved_by)

    def test_object_created_by_user_in_right_group_is_automatically_approved(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.professional_user)

        self.assertTrue(person.is_public)

    def test_object_created_by_superuser_is_automatically_approved(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.superuser)

        self.assertTrue(person.is_public)

    def test_save_prevents_volunteer_from_doing_object_approval(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
            is_public=True,
        )
        person.save(self.volunteer_user)

        person = Person.objects.all()[0]

        self.assertFalse(person.is_public)


class ModelCreationTest(BaseModerationTest):

    def test_create_person_populates_created_by(self):
        person = Person.objects.create(
            self.volunteer_user,
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )

        self.assertEqual(person.created_by, self.volunteer_user)

    def test_create_person_does_not_initially_populate_updated_by(self):
        person = Person.objects.create(
            self.volunteer_user,
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )

        self.assertIsNone(person.updated_by)

    def test_create_person_does_not_allow_volunteer_to_approve(self):
        person = Person.objects.create(
            self.volunteer_user,
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
            is_public=True,
        )

        self.assertFalse(person.is_public)

    def test_update_is_public_to_true_populates_approved_by__for_users_in_right_group(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.professional_user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(self.professional_user)

        self.assertEqual(person.approved_by, self.professional_user)

    def test_update_is_public_to_true_populates_approved_by__for_superusers(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.superuser)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(self.superuser)

        self.assertEqual(person.approved_by, self.superuser)

    def test_update_is_public_to_true_doesnt_populate_approved_by__for_users_in_wrong_group(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(self.volunteer_user)

        self.assertIsNone(person.approved_by)

    def test_object_created_by_user_in_right_group_is_automatically_approved(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.professional_user)

        self.assertTrue(person.is_public)

    def test_object_created_by_superuser_is_automatically_approved(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.superuser)

        self.assertTrue(person.is_public)


class QuerySetTest(BaseModerationTest):

    def test_volunteer_user_can_see_unapproved_objects_they_created(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        self.assertItemsEqual([person], Person.objects.for_user(self.volunteer_user))

    def test_unapproved_objects_created_by_volunteer_are_not_public(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        self.assertFalse(Person.objects.public())

    def test_volunteer_user_can_see_unapproved_objects_they_created(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        self.assertItemsEqual([person], Person.objects.for_user(self.volunteer_user))

    def test_logged_in_volunteer_user_can_see_unapproved_objects_others_created(self):
        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(self.volunteer_user)

        # just using AnonymousUser here because being a 'volunteer' essentially
        # means you have no special permissions...
        self.assertItemsEqual([person], Person.objects.for_user(AnonymousUser()))

