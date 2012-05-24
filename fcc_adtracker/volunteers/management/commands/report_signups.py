from django.core.management.base import LabelCommand, CommandError
from volunteers.models import Signup

from mongoengine import *
from mongo_utils import serializer

import datetime
import csv
from optparse import make_option

class Command(LabelCommand):
    option_list = LabelCommand.option_list + (
        make_option('-f', '--file', default='volunteer_signups.csv', dest='filename', type="string",
                help='Set the destination path for the output file. This will overwrite an existing file'),
        make_option('-a', '--all', action="store_true", default=False, dest='output_all',
                help='Output all signups, not just the ones marked for sharing. Defaults to False'),
    )
    args = "[from_date] [to_date]"
    help = ("Build a report of volunteer signups. If no dates arguments are supplied, this will generate a report for the previous day's signups")
    date_format = '%Y-%m-%d'

    def parse_date(self, date_string):
        try:
            datetime_obj = datetime.datetime.strptime(date_string, self.date_format)
            return datetime_obj
        except ValueError as e:
            raise CommandError('Date is in incorrect format')

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 1))
        filename = options.get('filename')
        output_all = options.get('output_all')
        fields = ('email', 'firstname', 'lastname', 'phone', 'station', 'date_submitted', 'share_info')
        from_dt = self.parse_date(args[0]) if len(args) else datetime.datetime.today() - datetime.timedelta(days=1)
        to_dt = self.parse_date(args[1]) if len(args) > 1 else from_dt
        if to_dt < from_dt:
            raise CommandError('[from_date] must be older than [to_date]')

        start_dt = from_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = to_dt.replace(hour=23, minute=59, second=59, microsecond=999999)

        if verbosity >= 1: 
            self.stdout.write('Fetching signups from {start_dt} to {end_dt}\n'.format(start_dt=start_dt, end_dt=end_dt))

        signup_list = Signup.objects(Q(date_submitted__gte=start_dt) & Q(date_submitted__lte=end_dt)).order_by('-date_submitted')
        if not output_all:
            signup_list.filter(_share_info=True)
        
        if len(signup_list):
            writer = csv.DictWriter(open(filename, 'w'), fields)
            writer.writeheader()

            for signup in signup_list:
                output = {
                    'email': signup.email,
                    'firstname': signup.firstname,
                    'lastname': signup.lastname,
                    'phone': signup.phone,
                    'station': signup.broadcaster.callsign if signup.broadcaster else None,
                    'date_submitted': signup.date_submitted.strftime(self.date_format + '  %H:%M:%S'),
                    'share_info': signup._share_info
                }
                writer.writerow(output)            

            self.stdout.write('Data written to "%s"\n' % filename)
        else:
            self.stdout.write('No signups for the given parameters\n')
