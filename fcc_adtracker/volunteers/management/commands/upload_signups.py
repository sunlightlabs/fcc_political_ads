from django.core.management.base import NoArgsCommand, CommandError
from volunteers.models import Signup
from django.conf import settings

from mongoengine import *
from mongo_utils import serializer

import csv
from tempfile import NamedTemporaryFile
from optparse import make_option

import gdata.docs.client
import gdata.docs.data
import gdata.data

GOOGLE_DOCS_ACCOUNT = getattr(settings, 'GOOGLE_DOCS_ACCOUNT', None)
GOOGLE_DOCS_PASSWORD = getattr(settings, 'GOOGLE_DOCS_PASSWORD', None)
GOOGLE_DOCS_RESOURCE_ID = getattr(settings, 'GOOGLE_DOCS_RESOURCE_ID', None)

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('-a', '--all', action="store_true", default=False, dest='output_all',
                help='Output all signups, not just the ones marked for sharing. Defaults to False'),
    )
    help = ("Upload a report of volunteer signups. Currently only goes to Google Docs.")

    def google_docs_handler(fileobj):
        pass

    def handle(self, *args, **options):
        if not GOOGLE_DOCS_ACCOUNT and GOOGLE_DOCS_PASSWORD and GOOGLE_DOCS_RESOURCE_ID:
            raise CommandError('You must set both GOOGLE_DOCS_ACCOUNT, GOOGLE_DOCS_PASSWORD and GOOGLE_DOCS_RESOURCE_ID in your settings file.')
        verbosity = int(options.get('verbosity', 1))
        output_all = options.get('output_all')
        fields = ('email', 'firstname', 'lastname', 'phone', 'city', 'state', 'station', 'date_submitted', 'share_info')


        signup_list = Signup.objects.all().order_by('-date_submitted')
        if not output_all:
            signup_list.filter(_share_info=True)

        if len(signup_list):
            fp = NamedTemporaryFile(delete=False)
            writer = csv.DictWriter(fp, fields)
            writer.writeheader()

            for signup in signup_list:
                output = {
                    'email': signup.email,
                    'firstname': signup.firstname,
                    'lastname': signup.lastname,
                    'phone': signup.phone,
                    'city': signup.city,
                    'state': signup.state,
                    'station': signup.broadcaster.callsign if signup.broadcaster else None,
                    'date_submitted': signup.date_submitted.strftime('%m/%d/%Y %H:%M:%S'),
                    'share_info': signup._share_info
                }
                writer.writerow(output)
            del(writer)

            client = gdata.docs.client.DocsClient()
            login_token = client.ClientLogin(GOOGLE_DOCS_ACCOUNT, GOOGLE_DOCS_PASSWORD, 'politicaladsleuth')

            fp.close()
            media = gdata.data.MediaSource(file_path=fp.name, content_type='text/csv')
            try:
                resource = client.get_resource_by_id(GOOGLE_DOCS_RESOURCE_ID)
                updated_resource = client.update_resource(resource, media=media,update_metadata=False, new_revision=True)
                self.stdout.write('Data uploaded to "%s"\n'.format(updated_resource.title.text))
            except gdata.client.RequestError as e:
                self.stderr.write(e.message + '\n')
                self.stdout.write('****Upload may have succeeded despite an InvalidEntryException error****\n')


            fp.unlink(fp.name)
        else:
            self.stdout.write('No signups for the given parameters\n')
