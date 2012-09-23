from haystack.views import SearchView, FacetedSearchView, search_view_factory

from django.utils.http import urlencode


class ImprovedFacetedSearchView(FacetedSearchView):
    def __name__(self):
        return "ImprovedFacetedSearchView"

    def extra_context(self):
        extra = super(ImprovedFacetedSearchView, self).extra_context()
        facet_tuple = tuple([item.split(':') for item in self.request.GET.getlist('selected_facets')])
        facet_dict = dict([(item[0].rstrip('_exact'),item[1]) for item in facet_tuple])
        extra['selected_facets'] = facet_dict
        extra['sfapp_base_template'] = 'sfapp/base-full.html'

        return extra