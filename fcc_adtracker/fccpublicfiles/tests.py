from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from broadcasters.models import Broadcaster
from doccloud.models import Document
from fccpublicfiles.models import PoliticalBuy
from mock import patch
from moderation.helpers import automoderate
import os.path


class DocFormTests(TransactionTestCase):

    def setUp(self):
        self.super_user = User(username='boss', first_name='Big', last_name='Boss', email='arowland@sunlightfoundation.com', is_active=True, is_staff=True, is_superuser=True)

        contributor_group = Group(name='Sunlight Contributors')
        contributor_group.save()

        self.contributor_user = User(
            username='joe_contributor',
            first_name='Joe',
            last_name='Contributor',
            email='arowland@sunlightfoundation.com',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        self.contributor_user.set_password('abc123')
        self.contributor_user.save()
        self.contributor_user.groups.add(contributor_group)

        #self.non_contributor_user = User(
        #    username='joe',
        #    first_name='Joe',
        #    last_name='Schmoe',
        #    email='arowland@sunlightfoundation.com',
        #    is_active=True,
        #    is_staff=False,
        #    is_superuser=False,
        #)
        #self.non_contributor_user.set_password('abc123')
        #self.non_contributor_user.save()

        Broadcaster.objects.bulk_create([
            Broadcaster(
                id=1,
                callsign='WFOX',
                channel=5,
                nielsen_dma='NY/NJ/CT',
                network_affiliate='New York Fox Network',
                facility_type='ABC',
                community_city='New York',
                community_state='NY',
            ),
            Broadcaster(
                id=2,
                callsign='WNBC',
                channel=4,
                nielsen_dma='NY/NJ/CT',
                network_affiliate='New York NBC Affiliate',
                facility_type='BCD',
                community_city='New York',
                community_state='NY',
            ),
        ])

        self.client.login(username=self.contributor_user.username, password='abc123')

    def test_display_form(self):
        url = reverse('document_submit')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document_submit.html')
        self.assertContains(response, "Broadcasters")

    def test_upload(self):
        url = reverse('document_submit')
        count = Document.objects.count()
        pb_count = PoliticalBuy.objects.count()

        with open(os.path.expanduser('~/tmp/test.pdf'), 'rb') as file_:
            with patch('doccloud.models.put_file') as put_file_mock:
                put_file_mock.return_value = (101, 'http://example.com/test.pdf')
                response = self.client.post(url, {
                    'broadcasters': [1],
                    'file': file_,
                    'user': self.contributor_user.pk,
                }, follow=True)

        self.approve_all_of_type(PoliticalBuy)
        #self.approve_all_of_type(Document)

        self.assertEqual(Document.objects.count(), count + 1)
        self.assertEqual(PoliticalBuy.objects.count(), pb_count + 1)

        self.assertTemplateUsed(response, 'document_success.html')
        self.assertContains(response, "Success")

        pb = PoliticalBuy.objects.all()[0]
        self.assertEqual(pb.broadcasters.count(), 1)

    def test_upload_with_multiselected_broadcasters(self):
        url = reverse('document_submit')
        count = Document.objects.count()

        with open(os.path.expanduser('~/tmp/test.pdf'), 'rb') as file_:
            with patch('doccloud.models.put_file') as put_file_mock:
                put_file_mock.return_value = (101, 'http://example.com/test.pdf')
                response = self.client.post(url, {
                    'broadcasters': [1, 2],
                    'file': file_,
                    'user': self.contributor_user.pk,
                }, follow=True)

        self.approve_all_of_type(PoliticalBuy)
        #self.approve_all_of_type(Document)

        self.assertEqual(Document.objects.count(), count + 1)
        self.assertTemplateUsed(response, 'document_success.html')
        self.assertContains(response, "Success")

        pb = PoliticalBuy.objects.all()[0]
        self.assertEqual(pb.broadcasters.count(), 1)

    def approve_all_of_type(self, model_class):
        for x in model_class.objects.all():
            automoderate(x, self.super_user)
