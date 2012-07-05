from ajax_select import LookupChannel
from django.db.models import Q
from .models import *
from doccloud.models import Document


class SaneLookupChannel(LookupChannel):
    min_length = 3


class AddressLookup(SaneLookupChannel):
    model = Address

    def get_query(self, q, request):
        return Address.objects.filter(Q(address1__startswith=q))


class PersonLookup(SaneLookupChannel):
    """Lookup a person by full name or common parts"""
    model = Person

    def get_query(self, q, request):
        name_parts = q.split(' ')
        if len(name_parts) == 1:
            return Person.objects.filter(Q(first_name__icontains=name_parts[0]) | Q(last_name__icontains=name_parts[0])).order_by('first_name', 'last_name')
        else:
            return Person.objects.filter(Q(first_name__icontains=name_parts[0]) & (Q(last_name__icontains=name_parts[1]) | Q(middle_name__icontains=name_parts[1]))).order_by('first_name', 'last_name')


class RoleTitleLookup(SaneLookupChannel):
    """lookup a role title from the Role object's title field"""
    model = Role

    def get_query(self, q, request):
        return Role.objects.filter(Q(title__startswith=q)).distinct('title').only('title')

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj.title)

    def get_result(self, obj):
        return obj.title


class OrganizationLookup(SaneLookupChannel):
    model = Organization

    def get_query(self, q, request):
        return Organization.objects.filter(name__icontains=q)


class AdvertiserLookup(OrganizationLookup):
    """Lookup an Advertiser organiztion"""
    def get_query(self, q, request):
        return Organization.objects.filter(name__icontains=q, organization_type=ORGANIZATION_TYPES[1][0])


class MediaBuyerLookup(OrganizationLookup):
    """Lookup a MediaBuyer organiztion"""
    def get_query(self, q, request):
        return Organization.objects.filter(name__icontains=q, organization_type=ORGANIZATION_TYPES[0][0])


class ShowNameLookup(SaneLookupChannel):
    model = PoliticalSpot

    def get_query(self, q, request):
        return PoliticalSpot.objects.filter(show_name__icontains=q).distinct('show_name').only('show_name')

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj.show_name)

    def get_result(self, obj):
        return obj.show_name


class DocumentCloudLookup(LookupChannel):
    model = Document
    min_length = 2

    def get_query(self, q, request):
        return Document.objects.filter(title__icontains=q)
