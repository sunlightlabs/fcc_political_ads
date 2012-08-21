from django.core.management.base import NoArgsCommand, CommandError
from volunteers.models import Signup
from django.conf import settings

from mongoengine import connect
from pymongo.database import Database
from pymongo.dbref import DBRef
from bson.objectid import ObjectId
import re

import csv
from tempfile import NamedTemporaryFile
from optparse import make_option

import gdata.docs.client
import gdata.docs.data
import gdata.data

GOOGLE_DOCS_ACCOUNT = getattr(settings, 'GOOGLE_DOCS_ACCOUNT', None)
GOOGLE_DOCS_PASSWORD = getattr(settings, 'GOOGLE_DOCS_PASSWORD', None)
GOOGLE_DOCS_RESOURCE_ID = getattr(settings, 'GOOGLE_DOCS_RESOURCE_ID', None)

MONGO_DATABASE = getattr(settings, 'MONGO_DATABASE')
MONGO_HOST = getattr(settings, 'MONGO_HOST')
MONGO_PORT = getattr(settings, 'MONGO_PORT')
MONGO_USERNAME = getattr(settings, 'MONGO_USERNAME')
MONGO_PASSWORD = getattr(settings, 'MONGO_PASSWORD')


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('-a', '--all', action="store_true", default=False, dest='output_all',
                help='Output all signups, not just the ones marked for sharing. Defaults to False'),
        make_option('-n', '--dry-run', action="store_true", default=False, dest='dry_run',
                help='Iterate over the objects, but do not upload. Useful with verbosity > 1'),
    )
    help = ("Upload a report of volunteer signups. Currently only goes to Google Docs.")

    def google_docs_handler(fileobj):
        pass

    def handle(self, *args, **options):
        if not GOOGLE_DOCS_ACCOUNT and GOOGLE_DOCS_PASSWORD and GOOGLE_DOCS_RESOURCE_ID:
            raise CommandError('You must set both GOOGLE_DOCS_ACCOUNT, GOOGLE_DOCS_PASSWORD and GOOGLE_DOCS_RESOURCE_ID in your settings file.')
        verbosity = int(options.get('verbosity', 1))
        dry_run = int(options.get('dry_run', 1))
        output_all = options.get('output_all')
        fields = ('email', 'firstname', 'lastname', 'phone', 'city', 'state', 'zipcode', 'station', 'date_submitted', 'share_info')

        signup_list = Signup.objects.all().order_by('-date_submitted')
        if not output_all:
            signup_list.filter(_share_info=True)

        if len(signup_list):
            dbref_pattern = r"^DBRef\(u'(?P<collection>\w*)', ObjectId\('(?P<object_id>\w*)'\)\)$"
            prog = re.compile(dbref_pattern)
            if not dry_run:
                fp = NamedTemporaryFile(delete=False)
                writer = csv.DictWriter(fp, fields)
                writer.writeheader()

            conn = connect(MONGO_DATABASE, host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME, password=MONGO_PASSWORD)
            db = Database(conn, MONGO_DATABASE)
            for signup in signup_list:
                if verbosity > 1:
                    self.stdout.write('Recording {0} whose share_info is {1}\n'.format(signup.email, signup._share_info))
                if signup.broadcaster:
                    if signup.broadcaster.startswith('DBRef'):
                        match_obj = prog.match(signup.broadcaster)
                        if match_obj:
                            match_dict = match_obj.groupdict()
                            ref = DBRef(match_dict.get('collection'), ObjectId(match_dict.get('object_id')))
                            br_doc = db.dereference(ref)
                            callsign = br_doc.get('callsign', '')
                        else:
                            callsign = ''
                    else:
                        callsign = signup.broadcaster
                else:
                    callsign = ''
                if verbosity > 1:
                    self.stdout.write('Recording callsign "{0}"\n'.format(callsign))
                output = {
                    'email': signup.email,
                    'firstname': signup.firstname,
                    'lastname': signup.lastname,
                    'phone': signup.phone,
                    'city': signup.city,
                    'state': signup.state,
                    'station': callsign,
                    'zipcode': signup.zipcode if signup.zipcode else None,
                    'date_submitted': signup.date_submitted.strftime('%m/%d/%Y %H:%M:%S'),
                    'share_info': signup._share_info
                }
                if verbosity > 2:
                    print(repr(output))
                if not dry_run:
                    writer.writerow(output)
            if not dry_run:
                del(writer)

            client = gdata.docs.client.DocsClient()
            login_token = client.ClientLogin(GOOGLE_DOCS_ACCOUNT, GOOGLE_DOCS_PASSWORD, 'politicaladsleuth')

            if not dry_run:
                fp.close()
                media = gdata.data.MediaSource(file_path=fp.name, content_type='text/csv')
                try:
                    resource = client.get_resource_by_id(GOOGLE_DOCS_RESOURCE_ID)
                    updated_resource = client.update_resource(resource, media=media, update_metadata=False, new_revision=True)
                    self.stdout.write('Data uploaded to "%s"\n'.format(updated_resource.title.text))
                except gdata.client.RequestError as e:
                    self.stderr.write(e.message + '\n')
                    self.stdout.write('****Upload may have succeeded despite an InvalidEntryException error****\n')

                fp.unlink(fp.name)
        else:
            self.stdout.write('No signups for the given parameters\n')
