#!/usr/bin/env python
# encoding: utf-8

import os, sys

projpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, projpath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fcc_adtracker.settings")

from django.template.defaultfilters import slugify
from fcc_adtracker import settings

BASIC_FIELDS = ('callsign', 'channel', 'nielsen_dma', 'network_affiliate', 'facility_type', 'community_city', 'community_state')

ADDRESS_FIELDS = ('address1', 'address2', 'city', 'state')

if __name__ == "__main__":

    from broadcasters.models import Broadcaster as OldBroadcaster
    from broadcasters.models import Address as OldAddress
    from fccpublicfiles.models import Broadcaster, Address, AddressLabel


    old_broadcasters = OldBroadcaster.objects.all()

    import ipdb; ipdb.set_trace()

    for counter, old_bc in enumerate(old_broadcasters):
        try:
            broadcaster = Broadcaster.objects.get(callsign=old_bc.callsign)
        except Broadcaster.DoesNotExist:
            broadcaster = Broadcaster(callsign=old_bc.callsign)
        for field in BASIC_FIELDS:
            broadcaster.__setattr__(field, old_bc.__getattribute__(field))
        broadcaster.save()
        for old_address in old_bc.addresses:
            has_address = reduce(lambda x,y: (x|y), [old_address.__getattribute__(fname) != None for fname in ADDRESS_FIELDS])
            if has_address:
                kwargs = dict([(fname, old_address.__getattribute__(fname) or u'') for fname in ADDRESS_FIELDS])
                kwargs['city'] = kwargs['city'].title()
                kwargs['zipcode'] =  old_address.zip1
                new_address, address_created = Address.objects.get_or_create(**kwargs)
                address_label, a_label_created = AddressLabel.objects.get_or_create(name=old_address.title, slug=slugify(old_address.title))
                address_label.save()
                new_address.address_labels.add(address_label)
                new_address.save()
                broadcaster.addresses.add(new_address)
        if broadcaster.community_city:
            broadcaster.community_city = broadcaster.community_city.title()
        broadcaster.save()
        print(repr(broadcaster))
        # print(counter, counter%10 == 0)

