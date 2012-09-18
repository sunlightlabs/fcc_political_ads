from django.conf.urls import patterns, include, url
from haystack.query import SearchQuerySet
from haystack.views import SearchView, FacetedSearchView, search_view_factory
from haystack.forms import SearchForm

from search.forms import DateRangeSearchForm

sqs = SearchQuerySet().facet('advertiser').facet('bought_by').facet('station')

urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
            view_class=FacetedSearchView,
            template='search/search.html',
            searchqueryset=sqs,
            form_class=DateRangeSearchForm,
            results_per_page=20
        ), name='haystack_search'),
)
