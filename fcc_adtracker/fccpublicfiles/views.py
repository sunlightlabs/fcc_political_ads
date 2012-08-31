from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q
from django.forms import ModelForm
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from fccpublicfiles.forms import PrelimDocumentForm, PoliticalBuyFormFull
from doccloud.models import Document
from urllib2 import HTTPError


from .models import *

# try:
#     import simplejson as json
# except Exception, e:
#     import json


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

        if not obj_list:
            obj_list = get_values_for_model_field(model, fieldname)
    else:
        obj_list = []
    return HttpResponse(json.dumps(obj_list), content_type='application/javascript')


def politicalbuy_view(request, buy_id, template_name='politicalbuy_view.html'):
    obj = get_object_or_404(PoliticalBuy, id=buy_id)
    return render(request, template_name, {'obj': obj})


@login_required
@transaction.commit_on_success
def prelim_doc_form(request, template_name='document_submit.html'):

    form = PrelimDocumentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save(commit=False)
        uploaded_file = request.FILES['file']

        # make the doccloud model
        cloud_doc = Document(
            file=uploaded_file,
            title=uploaded_file.name,
            user=request.user,
        )
        # upload
        cloud_doc.connect_dc_doc()
        cloud_doc.save()

        pol_buy = PoliticalBuy(
            documentcloud_doc=cloud_doc
        )
        pol_buy.save()

        pol_buy.broadcasters = form.cleaned_data['broadcasters']
        pol_buy.save()

        return redirect('document_success')

    return render(request, template_name, {'form': form})


def doc_success(request, template_name='document_success.html'):
    return render(request, template_name)


@login_required
def politicalbuy_edit(request, buy_id, template_name='politicalbuy_edit.html'):
    myobject = get_object_or_404(PoliticalBuy, pk=buy_id)

    form = PoliticalBuyFormFull(request.POST or None, instance=myobject)

    if form.is_valid():
        myobject = form.save()
        myobject.save()
        #return redirect('contributor_dashboard')
        return redirect('politicalbuy_view')

    return render(request, template_name, {'form': form, 'obj': myobject})

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

