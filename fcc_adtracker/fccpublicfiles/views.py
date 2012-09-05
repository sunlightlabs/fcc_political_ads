from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from fccpublicfiles.forms import PrelimDocumentForm, PoliticalBuyFormFull
from doccloud.models import Document

from .models import *


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

    return render(request, template_name, {'form': form, 'obj': myobject})

