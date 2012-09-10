from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from doccloud.models import Document

from .models import *
from fccpublicfiles.forms import PrelimDocumentForm, PoliticalBuyFormFull, SimpleOrganizationForm


def politicalbuy_view(request, buy_id, slug='', template_name='politicalbuy_view.html'):
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

        return redirect('user_dashboard')

    return render(request, template_name, {'form': form})


@login_required
def politicalbuy_edit(request, buy_id, template_name='politicalbuy_edit.html'):
    myobject = get_object_or_404(PoliticalBuy, pk=buy_id)

    form = PoliticalBuyFormFull(request.POST or None, instance=myobject)

    if form.is_valid():
        myobject = form.save()
        myobject.save()

    return render(request, template_name, {'form': form, 'obj': myobject})


@login_required
def handlePopAdd(request, addForm, field, initial_data=None):
    """ Using methods adapted from:
         http://sontek.net/blog/detail/implementing-djangos-admin-interface-pop-ups
         and
         http://www.awebcoder.com/post/16/djangos-admin-related-objects-pop-up-in-the-front-end
    """
    if request.method == "POST":
        form = addForm(request.POST, instance=initial_data)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError, error:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(newObject._get_pk_val()), escape(newObject)))
    else:
        form = addForm(instance=initial_data)

    pageContext = {'form': form, 'field': field}
    return render(request, 'add_model_view.html', pageContext)


@login_required
def add_advertiser(request):
    org_defaults = Organization(organization_type='AD')
    return handlePopAdd(request, SimpleOrganizationForm, 'advertiser', initial_data=org_defaults)


@login_required
def add_media_buyer(request):
    org_defaults = Organization(organization_type='MB')
    return handlePopAdd(request, SimpleOrganizationForm, 'mediabuyer', initial_data=org_defaults)
