from django.core.management.base import NoArgsCommand
from django.core.exceptions import ValidationError
# from django.conf import settings

# from optparse import make_option

from broadcasters.models import Broadcaster

from doccloud.models import Document

from fccpublicfiles.models import PoliticalBuy


class Command(NoArgsCommand):
    help = """Create PoliticalBuys from DocumentCloud Documents"""
    can_import_settings = True

    def handle_noargs(self, **options):
        orphan_docs = Document.objects.filter(politicalbuy__isnull=True)
        self.stdout.write('Found {0} orphan docs (not attached to PoliticalBuy records)\n'.format(orphan_docs.count()))
        for orphan_obj in orphan_docs:
            doc_meta = orphan_obj.dc_data
            callsign = doc_meta.get('callsign')
            if callsign is None:
                self.stderr.write('No callsign on "{0}". Skipping...\n'.format(orphan_obj.title))
                continue
            try:
                broadcaster = Broadcaster.objects.get(callsign__startswith=callsign)
            except Broadcaster.DoesNotExist:
                self.stderr.write("Can't find a Broadcaster with a callsign that matches {0}. Skipping...\n".format(broadcaster.callsign))
                continue
            except Broadcaster.MultipleObjectsReturned:
                self.stderr.write("document's callsign, {0}, matches multiple broadcasters. Skipping...\n".format(broadcaster.callsign))
                continue
            else:
                try:
                    pb_obj = PoliticalBuy(documentcloud_doc=orphan_obj)
                    pb_obj.broadcasters.add(broadcaster)
                    try:
                        pb_obj.full_clean()
                    except ValidationError, e:
                        self.stderr.write(e)
                    pb_obj.save()
                except Exception, e:
                    self.stderr.write(repr(e))
                    raise e
            self.stdout.write('"{0}"" is associated with station "{1}"\n'.format(orphan_obj.title, callsign))
