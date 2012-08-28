from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings

from volunteers.models import NonUserProfile

try:
    import unicodecsv as csv
except ImportError:
    import csv
from tempfile import NamedTemporaryFile
from optparse import make_option

import gdata.docs.client
import gdata.docs.data
import gdata.data

GOOGLE_DOCS_ACCOUNT = getattr(settings, 'GOOGLE_DOCS_ACCOUNT', None)
GOOGLE_DOCS_PASSWORD = getattr(settings, 'GOOGLE_DOCS_PASSWORD', None)
GOOGLE_DOCS_RESOURCE_ID = getattr(settings, 'GOOGLE_DOCS_RESOURCE_ID', None)

SIGNUP_EXTRA_FIELDS = getattr(settings, 'SIGNUP_EXTRA_FIELDS', ())


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('-a', '--all', action="store_true", default=False, dest='output_all',
                help='Output all signups, not just the ones marked for sharing. Defaults to False'),
        make_option('-n', '--dry-run', action="store_true", default=False, dest='dry_run',
                help='Dry run. Generate CSV data and send to stdout (do not upload)'),
    )
    help = ("Upload a report of volunteer signups. Currently only goes to Google Docs.")

    def google_docs_handler(fileobj):
        pass

    def handle(self, *args, **options):
        if not GOOGLE_DOCS_ACCOUNT and GOOGLE_DOCS_PASSWORD and GOOGLE_DOCS_RESOURCE_ID:
            raise CommandError('You must set both GOOGLE_DOCS_ACCOUNT, GOOGLE_DOCS_PASSWORD and GOOGLE_DOCS_RESOURCE_ID in your settings file.')
        verbosity = int(options.get('verbosity', 1))
        output_all = options.get('output_all')
        dry_run = options.get('dry_run')
        fields = ('email', 'first_name', 'last_name', 'phone', 'city', 'state', 'zipcode', 'is_a', 'broadcasters', 'date_created', 'share_info')

        profile_list = NonUserProfile.objects.order_by('-date_created')
        if not output_all:
            profile_list = profile_list.filter(share_info=True)

        if len(profile_list):
            if verbosity > 1:
                self.stdout.write('{0} signups to record.'.format(len(profile_list)))
            fp = NamedTemporaryFile(delete=False)
            writer = csv.DictWriter(fp, fields)
            writer.writeheader()

            for signup in profile_list:
                output = {
                    'email': signup.email,
                    'first_name': signup.first_name,
                    'last_name': signup.last_name,
                    'phone': signup.phone,
                    'city': signup.city,
                    'state': signup.state,
                    'zipcode': signup.zipcode,
                    'is_a': signup.is_a,
                    'date_created': signup.date_created.strftime('%m/%d/%Y %H:%M:%S'),
                    'share_info': signup.share_info
                }
                extra_fields_data = signup.extra_fields
                for extra_field in SIGNUP_EXTRA_FIELDS:
                    input_val = None
                    if isinstance(extra_fields_data[extra_field], list):
                        input_val = ', '.join(extra_fields_data[extra_field])
                    else:
                        input_val = extra_fields_data[extra_field]
                    output[extra_field] = input_val
                writer.writerow(output)
            if dry_run:
                self.stdout.write('Row created:\n{0}\n'.format('|'.join([str(output[f]) for f in fields])))
            del(writer)

            if not dry_run:
                client = gdata.docs.client.DocsClient()
                login_token = client.ClientLogin(GOOGLE_DOCS_ACCOUNT, GOOGLE_DOCS_PASSWORD, 'politicaladsleuth')
                fp.close()
                media = gdata.data.MediaSource(file_path=fp.name, content_type='text/csv')
                try:
                    resource = client.get_resource_by_id(GOOGLE_DOCS_RESOURCE_ID)
                    updated_resource = client.update_resource(resource, media=media, update_metadata=False, new_revision=True)
                    self.stdout.write('Data uploaded to "%s"\n'.format(updated_resource.title.text))
                except gdata.client.RequestError as e:
                    self.stderr.write(e.message + '\n')
                    self.stdout.write('****Upload may have succeeded despite an InvalidEntryException error****\n')

            fp.close()
            fp.unlink(fp.name)
        else:
            self.stdout.write('No signups for the given parameters\n')
