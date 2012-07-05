from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from optparse import make_option
import re
import copy
from time import sleep

from doccloud.models import get_client

DOCUMENTCLOUD_META = getattr(settings, 'DOCUMENTCLOUD_META', {})
DOCUMENTCLOUD_PROJECT_ID = getattr(settings, 'DOCUMENTCLOUD_PROJECT_ID')

CALLSIGN_REG = r'\b((W|K)[A-Z]{2,3}((-|\s)[A-Z]{2})?)\b'


class Command(BaseCommand):
    args = '<search_string ...>'
    help = 'Update the metadata on DocumentCloud docs with fccpublicfiles data k:v pairs'
    can_import_settings = True

    option_list = BaseCommand.option_list + (
        make_option('--project-add',
                    action='store_true',
                    dest='add_to_project',
                    default=False,
                    help='Add the documents to the project defined by settings.DOCUMENTCLOUD_PROJECT_ID'),
        make_option('--overwrite-data',
                    action='store_false',
                    dest='overwrite_data',
                    default=False,
                    help='Overwrite existing key,value pairs. Default behavior is to preserve existing k,v pairs.'),
        make_option('-n', '--dry-run',
                    action='store_true',
                    dest='dry_run',
                    default=False,
                    help='Run the script, but do not actually save the results'),
    )

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must pass one or more search strings')

        add_to_project = options.get('add_to_project')
        overwrite_data = options.get('overwrite_data')
        dry_run = options.get('dry_run')
        client = get_client()
        prog = re.compile(CALLSIGN_REG)
        project = client.projects.get_by_id(DOCUMENTCLOUD_PROJECT_ID) if DOCUMENTCLOUD_PROJECT_ID else None
        project_size = len(project.document_list)

        if dry_run:
            self.stdout.write('Dry run. Documents will not be updated.\n')

        for search_string in args:
            self.stdout.write('Search on "{0}"...  '.format(search_string))
            document_list = client.documents.search(search_string)
            self.stdout.write('Found {0} documents.\n'.format(len(document_list)))
            for doc in document_list:
                self.stdout.write('Processing doc: "{0}"... '.format(doc.id))
                if add_to_project:
                    if doc.id not in project.document_ids:
                        self.stdout.write('Adding doc to project "{project_title}"\n'.format(project_title=project.title))
                        if not dry_run:
                            project.document_list.append(doc)
                    else:
                        self.stdout.write('Doc exists in project "{0}"\n'.format(project.title))
                else:
                    self.stdout.write('\n')
                match_obj = prog.search(doc.title)
                callsign = match_obj.group(1).strip().replace(' ', '-') if hasattr(match_obj, 'group') else None
                new_data = copy.deepcopy(DOCUMENTCLOUD_META)
                if callsign:
                    self.stdout.write('Found possible callsign "{callsign}" in the title: "{title}"\n'.format(callsign=callsign, title=doc.title))
                    new_data.update({'callsign': callsign})
                doc_data = copy.deepcopy(doc.data)
                if overwrite_data:
                    doc_data.update(new_data)
                else:
                    for key, value in new_data.iteritems():
                        if key not in doc_data:
                            doc_data[key] = value
                if doc.data != doc_data:
                    if not dry_run:
                        doc.data = doc_data
                        doc.put()
                        sleep(0.125)  # Not sure if this is necessary, but let's play nice-ish
                else:
                    self.stdout.write('The doc data is already up to date. There are no data changes to push\n')
                self.stdout.write('\n')

        if add_to_project:
            new_size = len(project.document_list)
            new_count = new_size - project_size
            if dry_run:
                self.stdout.write('SIMULATING: ')
            self.stdout.write('Updating project document list... Adding {0} documents. '.format(new_count))
            if project_size != new_size:
                self.stdout.write('Project document count from {0} to {1}]\n'.format(project_size, new_size))
            if not dry_run:
                project.put()
            self.stdout.write('\n')
