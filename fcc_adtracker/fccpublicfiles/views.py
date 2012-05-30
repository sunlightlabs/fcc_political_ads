from django.http import HttpResponse
from django.db.models import Q, F


from .models import *

try:
    import simplejson as json
except Exception, e:
    import json


POLITICALBUY_WHITELIST = ('advertiser', 'advertiser_signatory', 'ordered_by')
POLITICALSPOT_WHITELIST = ('show_name',)
STATION_WHITELIST = ('station',)

def get_values_for_model_field(model, fieldname):
    exclude_query = Q(**{'{0}__isnull'.format(fieldname): True}) | Q(**{fieldname: ''})
    return [obj.__getattribute__(fieldname) for obj in model.objects.exclude(exclude_query).only(fieldname)]


def admin_autocomplete_json(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=401, content_type='application/javascript')
    fieldname = request.GET.get('fieldname', None)
    obj_list = None
    if fieldname:
        model = None
        if fieldname in POLITICALBUY_WHITELIST:
            model = PoliticalBuy
        elif fieldname in POLITICALSPOT_WHITELIST:
            model = PoliticalSpot
        elif fieldname in STATION_WHITELIST:
            obj_list = [c[0] for c in CALLSIGNS]

        if not obj_list: obj_list = get_values_for_model_field(model, fieldname)
    else:
        obj_list = []
    return HttpResponse(json.dumps(obj_list), content_type='application/javascript')

# def admin_advertiser_list(request):
#     obj_list = get_values_for_model_field(PoliticalBuy, 'advertiser')
#     return HttpResponse(json.dumps(obj_list), content_type='application/javascript')

# def admin_advertiser_signatory_list(request):
#     obj_list = get_values_for_model_field(PoliticalBuy, 'advertiser_signatory')
#     return HttpResponse(json.dumps(obj_list), content_type='application/javascript')

# def admin_ordered_by_list(request):
#     obj_list = get_values_for_model_field(PoliticalBuy, 'ordered_by')
#     return HttpResponse(json.dumps(obj_list), content_type='application/javascript')

# def admin_show_name_list(request):
#     obj_list = get_values_for_model_field(PoliticalSpot, 'show_name')
#     return HttpResponse(json.dumps(obj_list), content_type='application/javascript')

