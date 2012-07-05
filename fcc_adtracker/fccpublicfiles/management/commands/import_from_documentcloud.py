from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

from tempfile import TemporaryFile
from optparse import make_option
import os.path

from doccloud.models import get_client, Document, DocumentCloudProperties

DOCUMENTCLOUD_META = getattr(settings, 'DOCUMENTCLOUD_META', {})
DOCUMENTCLOUD_PROJECT_ID = getattr(settings, 'DOCUMENTCLOUD_PROJECT_ID')


class Command(BaseCommand):
    args = '<unimplemented ...>'
    help = 'Create Document records in Django for entities that exist only in our DocumentCloud project.'
    can_import_settings = True
    option_list = BaseCommand.option_list + (
        make_option('-n', '--dry-run',
                    action='store_true',
                    dest='dry_run',
                    default=False,
                    help='Run the script, but do not actually save the results'),
    )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run')
        verbosity = options.get('verbosity', 1)

        if dry_run:
            self.stdout.write('Dry run. No new document records will be created.\n')

        client = get_client()
        self.stdout.write('Connecting to DocumentCloud...\n')
        project = client.projects.get(id=DOCUMENTCLOUD_PROJECT_ID) if DOCUMENTCLOUD_PROJECT_ID else None

        if project:
            self.stdout.write('Pulling document list for "{0}"...\n\n'.format(project.title))
            document_id_list = project.document_ids
            new_docs_list = []
            for doc_id in document_id_list:
                if verbosity > 1:
                    self.stdout.write('Checking "{0}"\n'.format(doc_id))
                try:
                    doc_obj = DocumentCloudProperties.objects.get(dc_id=doc_id)
                    if verbosity > 1 and doc_obj:
                        self.stdout.write('DocumentCloudProperties record for "{0}" already exists\n'.format(doc_id))
                except DocumentCloudProperties.DoesNotExist:
                    dc_obj = client.documents.get(id=doc_id)
                    new_doc_props = DocumentCloudProperties(dc_id=dc_obj.id, dc_url=dc_obj.canonical_url)
                    if verbosity > 1:
                        self.stdout.write('Creating record for {0}\n'.format(dc_obj.id))
                        if verbosity > 2:
                            self.stdout.write('with:\n\tTitle: {title}\n\tDescription {description}\n\tAccess: {access}\n'.format(
                                              title=dc_obj.title, description=dc_obj.description, access=dc_obj.access))
                    new_doc = Document(title=dc_obj.title,
                                       description=dc_obj.description,
                                       access_level=dc_obj.access)
                    filename = os.path.basename('{0}.pdf'.format(dc_obj.id))
                    if verbosity > 1:
                        self.stdout.write('Saving file named {0}\n'.format(filename))
                    if not dry_run:
                        fp = TemporaryFile()
                        djfp = File(fp)
                        djfp.write(dc_obj.pdf)
                        djfp.seek(0)
                    try:
                        if not dry_run:
                            new_doc.file.save(filename, djfp)
                            if not new_doc.file.closed:
                                new_doc.file.close()
                    except AttributeError as e:
                        if verbosity > 1:
                            self.stderr.write('Error saving doc:\n\t"{error_message}"\n'.format(error_message=repr(e)))
                            if new_doc.file.url and new_doc.file.url != '':
                                self.stdout.write("New file at:\n\t{0}\n".format(new_doc.file.url))
                        pass
                    if not dry_run:
                        djfp.close()
                        new_doc_props.save()
                        new_doc.dc_properties = new_doc_props
                        new_doc.save()
                    new_docs_list.append(doc_id)
                self.stdout.write('\n')
            self.stdout.write('Added {num_docs} new Document records (out of {num_dc_docs})\n'.format(num_docs=len(new_docs_list), num_dc_docs=len(document_id_list)))
        else:
            raise CommandError('No DOCUMENTCLOUD_PROJECT_ID set in settings. Cannot proceed\n')
