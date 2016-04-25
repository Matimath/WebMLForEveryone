from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from upload.models import Document
from upload.forms import UploadDocumentForm
from MLlib.MLlibAlpha import *

import json


# Create your views here.
def upload(request):
    # File upload
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Add new document
            doc = Document(docfile=request.FILES['docfile'])
            doc.save()
            # Reload page after POST
            return HttpResponseRedirect(reverse('choose', kwargs={'id': doc.id}))
    else:
        form = UploadDocumentForm()

    # Render page using model parameters
    return render(request, 'upload.html', {
        'form': form
    })


def choose(request, id):
    doc = Document.objects.get(id=id)
    path = doc.docfile.path
    columns = get_columns(path)
    return render(request, 'choose.html', {
        'id': doc.id,
        'columns': columns
    })


def ajax_choose_model(request):
    document_id = request.GET.get('document_id')
    column = request.GET.get('column')
    doc = get_object_or_404(Document, id=document_id)
    mb = ModelBuilder(doc.docfile.path, column)
    response_data = {}
    response_data['Model_type'] = mb.model_type.name
    response_data['Available_models'] = [{
                                             "Name": name.name
                                         } for name in Selected_model]
    return JsonResponse(response_data)


def ajax_predict(request):
    document_id = request.GET.get('document_id')
    column = request.GET.get('column')
    model = request.GET.get('model')
    doc = get_object_or_404(Document, id=document_id)
    mb = ModelBuilder(doc.docfile.path, column)
    mb.train_model(model)
    vec = request.GET.get('vec')
    vec = json.loads(vec)
    pred = mb.predict(vec)
    return HttpResponse(pred)


def compute(request, id, column, model):
    doc = Document.objects.get(id=id)
    path = doc.docfile.path
    columns = get_columns(path)
    input_columns = []
    for col in columns:
        if col != column:
            input_columns.append(col)
    return render(request, 'compute.html', {
        'id': doc.id,
        'column': column,
        'model': model,
        'columns': input_columns,
        'columns_length': len(input_columns)
    })
