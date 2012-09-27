from django.conf.urls import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

from search.views import ImprovedFacetedSearchView
from search.forms import DateRangeSearchForm

sqs_all = SearchQuerySet().facet('status').facet('type').facet('state').facet('advertiser').facet('station')
# sqs_public = sqs_all.filter(is_public=True)


urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
            view_class=ImprovedFacetedSearchView,
            template='search/search.html',
            searchqueryset=sqs_all,
            form_class=DateRangeSearchForm,
            results_per_page=20
        ), name='haystack_search'),
    # url(r'^auth$', search_view_factory(
    #         view_class=FacetedSearchView,
    #         template='search/search.html',
    #         searchqueryset=sqs_all,
    #         form_class=DateRangeSearchForm,
    #         results_per_page=20
    #     ), name='haystack_search'),
)
