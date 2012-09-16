from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from doccloud.models import Document

from .models import *
from fccpublicfiles.forms import PrelimDocumentForm, PoliticalBuyFormFull,\
        SimpleOrganizationForm, AdvertiserSignatoryForm, RelatedPoliticalSpotForm

from name_cleaver import IndividualNameCleaver


def politicalbuy_view(request, uuid_key, slug='', template_name='politicalbuy_view.html'):
    obj = get_object_or_404(PoliticalBuy, uuid_key=uuid_key)
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

        return redirect('user_dashboard')

    return render(request, template_name, {'form': form})


@login_required
def politicalbuy_edit(request, uuid_key, template_name='politicalbuy_edit.html'):
    myobject = get_object_or_404(PoliticalBuy, uuid_key=uuid_key)

    form = PoliticalBuyFormFull(request.POST or None, instance=myobject)
    if form.is_valid():
        myobject = form.save()
        myobject.save()

    return render(request, template_name, {'form': form, 'obj': myobject, 'sfapp_base_template': 'sfapp/base-full.html'})


@login_required
def handlePopAdd(request, addForm, field, initial_data=None, current_object=None):
    """ Using methods adapted from:
         http://sontek.net/blog/detail/implementing-djangos-admin-interface-pop-ups
         and
         http://www.awebcoder.com/post/16/djangos-admin-related-objects-pop-up-in-the-front-end
    """
    if request.method == "POST":
        form = addForm(request.POST, instance=current_object)
        if form.is_valid():
            try:
                obj = form.save()
            except forms.ValidationError:
                obj = None
            if obj:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(obj._get_pk_val()), escape(obj)))
    else:
        if current_object:
            form = addForm(instance=current_object)
        else:
            form = addForm(initial_data)
    pageContext = {'form': form, 'field': field}
    return render(request, 'add_model_view.html', pageContext)


@login_required
def edit_related_politicalspot(request, uuid_key, spot_id=None):
    if spot_id:
        try:
            current_obj = PoliticalSpot.objects.get(id=int(spot_id))
        except PoliticalSpot.DoesNotExist:
            current_obj =  None
    else:
        current_obj =  None
    initial_data = {
        'document': PoliticalBuy.objects.get(uuid_key=uuid_key)
    }
    if current_obj:
        initial_data['id'] = current_obj.id

    return handlePopAdd(request, RelatedPoliticalSpotForm, 'politicalspot', initial_data=initial_data, current_object=current_obj)


@login_required
def add_advertiser(request):
    org_defaults = {'organization_type': 'AD'}
    if 'search' in request.GET:
        org_defaults['name'] = request.GET['search']
    return handlePopAdd(request, SimpleOrganizationForm, 'advertiser', initial_data=org_defaults)


@login_required
def add_media_buyer(request):
    org_defaults = {'organization_type': 'MB'}
    if 'search' in request.GET:
        org_defaults['name'] = request.GET['search']
    return handlePopAdd(request, SimpleOrganizationForm, 'mediabuyer', initial_data=org_defaults)


@login_required
def add_advertiser_signatory(request):
    if 'advertiser_id' in request.GET:
        defaults = {
            'advertiser_id': request.GET['advertiser_id'] or None
        }
    else:
        defaults = {}
    if 'search' in request.GET:
        input_name = IndividualNameCleaver(request.GET['search']).parse(safe=True)
        if isinstance(input_name, basestring):
            defaults['first_name'] = input_name
        else:
            defaults['first_name'] = input_name.first
            defaults['middle_name'] = input_name.middle
            defaults['last_name'] = input_name.last
            defaults['suffix'] = input_name.suffix

    if request.method == "POST":
        form = AdvertiserSignatoryForm(request.POST)
        if form.is_valid():
            person = Person()
            person.first_name = form.data['first_name']
            person.middle_name = form.data.get('middle_name', None)
            person.last_name = form.data['last_name']
            person.suffix = form.data.get('suffix', None)
            person.save()
            if 'advertiser_id' in form.data:
                adv_id = form.data.get('advertiser_id', None)
                if adv_id:
                    try:
                        advertiser = Organization.objects.get(id=adv_id)
                        role = Role(person=person, organization=advertiser)
                        role.title = form.data.get('job_title', '')
                        role.save()
                    except Organization.DoesNotExist:
                        # What else to do in this case?
                        pass
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(person._get_pk_val()), escape(person)))
    return handlePopAdd(request, AdvertiserSignatoryForm, 'advertiser_signatory', initial_data=defaults)
