from django.test import TestCase
from django.contrib.auth.models import User, Group
from fccpublicfiles.models import Person
from broadcasters.models import Broadcaster
from mock import patch

import os.path
import unittest2


class ModelSaveTest(TestCase):

    def test_save_person_populates_created_by(self):
        user = User.objects.create(username='arowland')

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertEqual(person.created_by, user)

    def test_save_person_does_not_initially_populate_updated_by(self):
        user = User.objects.create(username='arowland')

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertIsNone(person.updated_by)

    def test_update_person_populates_updated_by(self):
        user = User.objects.create(username='arowland')

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        person.middle_name = 'Ignatius'

        person.save(user)

        self.assertEqual(person.updated_by, user)

    def test_update_is_public_to_true_populates_approved_by__for_users_in_right_group(self):
        user = User.objects.create(username='arowland')
        professionals = Group.objects.create(name='Professionals')
        user.groups.add(professionals)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(user)

        self.assertEqual(person.approved_by, user)

    def test_update_is_public_to_true_populates_approved_by__for_superusers(self):
        user = User.objects.create(username='arowland', is_superuser=True)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(user)

        self.assertEqual(person.approved_by, user)

    def test_update_is_public_to_true_doesnt_populate_approved_by__for_users_in_wrong_group(self):
        user = User.objects.create(username='arowland')
        volunteers = Group.objects.create(name='Volunteers')
        user.groups.add(volunteers)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(user)

        self.assertIsNone(person.approved_by)

    def test_object_created_by_user_in_right_group_is_automatically_approved(self):
        user = User.objects.create(username='arowland')
        group = Group.objects.create(name='Professionals')
        user.groups.add(group)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertTrue(person.is_public)

    def test_object_created_by_superuser_is_automatically_approved(self):
        user = User.objects.create(username='arowland', is_superuser=True)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertTrue(person.is_public)

    def test_save_prevents_volunteer_from_doing_object_approval(self):
        user = User.objects.create(username='arowland')
        group = Group.objects.create(name='Volunteers')
        user.groups.add(group)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
            is_public=True,
        )
        person.save(user)

        person = Person.objects.all()[0]

        self.assertFalse(person.is_public)


class ModelCreationTest(TestCase):

    def test_create_person_populates_created_by(self):
        user = User.objects.create(username='arowland')

        person = Person.objects.create(
            user,
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )

        self.assertEqual(person.created_by, user)

    def test_create_person_does_not_initially_populate_updated_by(self):
        user = User.objects.create(username='arowland')

        person = Person.objects.create(
            user,
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )

        self.assertIsNone(person.updated_by)

    def test_create_person_does_not_allow_volunteer_to_approve(self):
        user = User.objects.create(username='arowland')
        professionals = Group.objects.create(name='Volunteers')
        user.groups.add(professionals)

        person = Person.objects.create(
            user,
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
            is_public=True,
        )

        self.assertFalse(person.is_public)

    def test_update_is_public_to_true_populates_approved_by__for_users_in_right_group(self):
        user = User.objects.create(username='arowland')
        professionals = Group.objects.create(name='Professionals')
        user.groups.add(professionals)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(user)

        self.assertEqual(person.approved_by, user)

    def test_update_is_public_to_true_populates_approved_by__for_superusers(self):
        user = User.objects.create(username='arowland', is_superuser=True)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(user)

        self.assertEqual(person.approved_by, user)

    def test_update_is_public_to_true_doesnt_populate_approved_by__for_users_in_wrong_group(self):
        user = User.objects.create(username='arowland')
        volunteers = Group.objects.create(name='Volunteers')
        user.groups.add(volunteers)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        person.middle_name = 'Ignatius'
        person.is_public = True

        person.save(user)

        self.assertIsNone(person.approved_by)

    def test_object_created_by_user_in_right_group_is_automatically_approved(self):
        user = User.objects.create(username='arowland')
        group = Group.objects.create(name='Professionals')
        user.groups.add(group)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertTrue(person.is_public)

    def test_object_created_by_superuser_is_automatically_approved(self):
        user = User.objects.create(username='arowland', is_superuser=True)

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertTrue(person.is_public)


class QuerySetTest(TestCase):

    def test_volunteer_user_can_see_unapproved_objects_they_created(self):
        user = User.objects.create(username='arowland')
        group =Group.objects.create(name='Volunteers')
        user.groups.add(group)
        user.save()

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertItemsEqual([person], Person.objects.for_user(user))

    def test_unapproved_objects_created_by_volunteer_are_not_public(self):
        user = User.objects.create(username='arowland')
        group =Group.objects.create(name='Volunteers')
        user.groups.add(group)
        user.save()

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertFalse(Person.objects.public())

    def test_volunteer_user_can_see_unapproved_objects_they_created(self):
        user = User.objects.create(username='arowland')
        group =Group.objects.create(name='Volunteers')
        user.groups.add(group)
        user.save()

        person = Person(
            first_name='Joe',
            middle_name='Herbert',
            last_name='Schmoe',
            suffix='PhD',
        )
        person.save(user)

        self.assertItemsEqual([person], Person.objects.for_user(user))

    # TODO: this should *probably* pass as well, but doesn't... need to talk
    # to Dan and Jacob about this.
    #def test_volunteer_user_can_see_unapproved_objects_others_created(self):
    #    user = User.objects.create(username='arowland')
    #    group =Group.objects.create(name='Volunteers')
    #    user.groups.add(group)
    #    user.save()

    #    other_user = User.objects.create(username='joe')

    #    person = Person(
    #        first_name='Joe',
    #        middle_name='Herbert',
    #        last_name='Schmoe',
    #        suffix='PhD',
    #    )
    #    person.save(other_user)

    #    self.assertItemsEqual([person], Person.objects.for_user(user))

