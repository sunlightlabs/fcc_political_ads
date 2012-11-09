from haystack.views import FacetedSearchView
from django.contrib.localflavor.us import us_states

DATE_FIELDS = ('start_date', 'end_date')


class ImprovedFacetedSearchView(FacetedSearchView):
    def __name__(self):
        return "ImprovedFacetedSearchView"

    def extra_context(self):
        extra = super(ImprovedFacetedSearchView, self).extra_context()
        facet_tuple = tuple([item.split(':') for item in self.request.GET.getlist('selected_facets')])
        facet_dict = dict([(item[0].split('_exact')[0], item[1]) for item in facet_tuple if len(item) > 1])
        extra['selected_facets'] = facet_dict
        extra['date_filters'] = []
        for key, value in self.request.GET.iteritems():
            if key.startswith(DATE_FIELDS):
                extra['date_filters'].append((key, value))
        extra['date_filters'].sort()
        extra['us_states'] = us_states.US_STATES
        extra['sfapp_base_template'] = 'sfapp/base-full.html'

        return extra
