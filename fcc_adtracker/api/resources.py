from django.conf import settings
from django.conf.urls import url
from django.core.urlresolvers import NoReverseMatch
from django.core.paginator import InvalidPage
from django.http import Http404

from tastypie import fields
from tastypie.http import HttpBadRequest
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, Bundle
from tastypie.cache import SimpleCache
from tastypie.utils import trailing_slash
from tastypie.paginator import Paginator

from fccpublicfiles.models import PoliticalBuy
from haystack.query import SearchQuerySet

uuid_re_str = r'(?P<uuid_key>[a-f0-9-]{32,36})'

API_NAME = 'v1'

API_MAX_RESULTS_PER_PAGE = getattr(settings, 'API_MAX_RESULTS_PER_PAGE', 500)
API_LIMIT_PER_PAGE = getattr(settings, 'API_LIMIT_PER_PAGE', 20)

# Made methods that return lists of objects respect a max_limit meta option.


class PoliticalFileResource(ModelResource):
    class Meta:
        queryset = PoliticalBuy.objects.all()
        limit = API_LIMIT_PER_PAGE
        max_limit = API_MAX_RESULTS_PER_PAGE
        resource_name = 'politicalfile'
        api_name = API_NAME
        allowed_methods = ['get']
        cache = SimpleCache()
        paginator_class = Paginator
        fields = ('uuid_key', 'advertiser', 'contract_number', \
                  'contract_start_date', 'contract_end_date', \
                  'nielsen_dma', 'community_state', \
                  'candidate_type', 'upload_time', 'updated_at')

    nielsen_dma_id = fields.IntegerField(attribute='dma_id', null=True, blank=True)
    advertiser = fields.CharField()
    broadcasters = fields.ListField()
    doc_status = fields.CharField()
    total_spent = fields.DecimalField()
    num_spots = fields.IntegerField(attribute='num_spots_raw', null=True, blank=True)
    doc_source = fields.CharField()

    def dehydrate_advertiser(self, bundle):
        return bundle.obj.advertiser or None

    def dehydrate_contract_number(self, bundle):
        return bundle.obj.contract_number or None

    def dehydrate_broadcasters(self, bundle):
        return bundle.obj.broadcasters_callsign_list()

    def dehydrate_doc_status(self, bundle):
        return bundle.obj.doc_status()

    def dehydrate_total_spent(self, bundle):
        return bundle.obj.total_spent()

    def dehydrate_doc_source(self, bundle):
        return bundle.obj.doc_source()

    def base_urls(self):
        """
        ***
        Override:
            - exclude pk resources
        ***
        "The standard URLs this ``Resource`` should respond to."
        """
        # Due to the way Django parses URLs, ``get_multiple`` won't work without
        # a trailing slash.
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_schema'), name="api_get_schema"),
        ]

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>{0})/{1}/$".format(self._meta.resource_name, uuid_re_str), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>{0})/search/$".format(self._meta.resource_name), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
            'api_name': self._meta.api_name
        }
        if isinstance(bundle_or_obj, Bundle):
            kwargs['uuid_key'] = bundle_or_obj.obj.uuid_key
        else:
            kwargs['uuid_key'] = bundle_or_obj.uuid_key
        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

    def get_list(self, request, **kwargs):
        """
        ***
        Override:
            - Implements max_limit
        ***
        Returns a serialized list of resources.

        Calls ``obj_get_list`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        # TODO: Uncached for now. Invalidation that works for everyone may be
        #       impossible.
        objects = self.obj_get_list(request=request, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        req_data = request.GET.copy()
        limit = req_data.get('limit', self._meta.limit)
        if limit > self._meta.max_limit:
            limit = self._meta.max_limit
            req_data['limit'] = unicode(limit)
        paginator = self._meta.paginator_class(req_data, sorted_objects, resource_uri=self.get_resource_list_uri(), limit=limit)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [self.build_bundle(obj=obj, request=request) for obj in to_be_serialized['objects']]
        to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)

    def get_search_uri(self):
        """
        Returns a URL specific to this resource's search endpoint.
        """
        kwargs = {
            'resource_name': self._meta.resource_name,
            'api_name': self._meta.api_name
        }

        try:
            return self._build_reverse_url("api_get_search", kwargs=kwargs)
        except NoReverseMatch:
            return None

    def get_search(self, request, **kwargs):
        """
        Queries haystack search index and returns a serialized list of resources.
        """
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        query = request.GET.get('q', None)
        if not query:
            return self.create_response(request, BadRequest("Search endpoint requires an argument assigned to a 'q' query parameter"), response_class=HttpBadRequest)
        sqs = SearchQuerySet().models(PoliticalBuy).load_all().auto_query(query)

        # if 'start_date' in request.GET:
        #         start_date = request.GET.get('start_date', None)
        #         sqs = sqs.filter(start_date__gte=self.cleaned_data['start_date'])

        object_list = [search_result.object for search_result in sqs]

        req_data = request.GET.copy()
        limit = req_data.get('limit', self._meta.limit)
        if limit > self._meta.max_limit:
            limit = self._meta.max_limit
            req_data['limit'] = unicode(limit)
        paginator = Paginator(req_data, object_list, resource_uri=self.get_search_uri(), limit=limit)

        try:
            to_be_serialized = paginator.page()
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        bundles = [self.build_bundle(obj=obj, request=request) for obj in to_be_serialized['objects']]
        to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)

        self.log_throttled_access(request)
        return self.create_response(request, to_be_serialized)
