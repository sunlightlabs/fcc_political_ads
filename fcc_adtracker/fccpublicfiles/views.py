from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q
from django.forms import ModelForm
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, render, redirect
from fccpublicfiles.forms import PrelimDocumentForm
#from doccloud.forms import DocCloudDocForm
from doccloud.models import Document as DocCloudDocument
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


@login_required
@transaction.commit_on_success
def prelim_doc_form(request, template_name='document_submit.html'):

    form = PrelimDocumentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save(commit=False)
        uploaded_file = request.FILES['file']

        # make the doccloud model
        try:
            cloud_doc = DocCloudDocument(
                file=uploaded_file,
                title=uploaded_file.name,
                user=request.user,
            )
            # do the actual upload
            cloud_doc.connect_dc_doc()

            cloud_doc.save()

        except HTTPError, e:
            messages.error(request, 'Error: Something went wrong with your request. It appears your Document Cloud upload did not complete. Please try again.')
            return redirect('document_submit')

        except Exception, e:
            messages.error(request, 'Error: Oh no, something went terribly wrong with your document upload.')
            raise e

        # make our model
        try:
            pub_doc = PublicDocument.objects.create(
                documentcloud_doc=cloud_doc,

            )
            #import pdb; pdb.set_trace();
            #choices = [ x for x in form.fields['broadcasters'].choices ]
            #print choices

        except Exception, e:
            messages.error(request, 'Error: Oh no, something went wrong with the document creation on our system.')
            raise e

        try:

            form.save_m2m()
            #[ pub_doc.broadcasters.add(x[0]) for x in form.fields['broadcasters'].choices ]
            #pub_doc.save()

            #pub_doc.save_m2m()

        except Exception, e:
            messages.error(request, 'Error: Oh no, something went wrong with saving the broadcasters.')
            raise e

        return redirect('document_success')

    #from django.forms.models import inlineformset_factory
    #DoccloudFormset = inlineformset_factory(Document)

    return render(request, template_name, {'form': form})


def doc_success(request, template_name='document_success.html'):

    return render(request, template_name)

#@login_required
#def upload(request, template_name='doccloud-upload.html'):
#    context = {}
#    try:
#
#        # if form has already been submitted , do stuff
#        if request.method == 'POST':
#            dc_form = DocCloudDocForm(request.POST, request.FILES)
#            dc_form.user = request.user
#
#            # if form is valid, submit to documentcloud
#            if dc_form.is_valid():
#                model = dc_form.save(commit=False)
#                # user field can be null so login not necessarily required
#                # model.user = request.user
#                model.connect_dc_doc()  # queue for background processing here
#                model.save()
#                return redirect('docs_list')
#
#            # otherwise, re-render form
#            else:
#                context['form'] = dc_form
#                return render_to_response('upload.html',
#                                          context,
#                                          context_instance=RequestContext(request))
#        # otherwise, merely render template
#        else:
#            return render_to_response('upload.html',
#                                      context,
#                                      context_instance=RequestContext(request))
#    except Exception as e:
#        print e  # need logger
#    return render_to_response(template_name,
#                              context,
#                              context_instance=RequestContext(request))


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

