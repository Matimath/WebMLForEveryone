from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404

from upload.models import Document
from upload.forms import UploadDocumentForm
from MLlib.MLlibAlpha import *
from django.conf import settings

import pickle
import json
import time


def current_milli_time():
    return str(int(round(time.time() * 1000)))


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
    doc = get_object_or_404(Document, id=id)
    path = doc.docfile.path
    columns = get_columns(path)
    return render(request, 'choose.html', {
        'id': doc.id,
        'columns': columns
    })


def compute(request, model_builder):
    id = request.GET.get('id')

    mb = pickle.load(open(settings.MEDIA_ROOT + "/pickle/" + model_builder + ".mb", "rb"))
    path = mb.file_path
    column = mb.target_column

    columns = get_columns(path)
    input_columns = []
    column_index = -1
    for i, col in enumerate(columns):
        if col == column:
            column_index = i
        input_columns.append({
            'data': col,
            'type': 'text',
            'name': col
        })
    return render(request, 'compute.html', {
        'id': id,
        'model_builder': model_builder,
        'columns': input_columns,
        'columns_length': len(input_columns),
        'column_index': column_index
    })


def ajax_choose_model(request):
    document_id = request.GET.get('document_id')
    column = request.GET.get('column')
    doc = get_object_or_404(Document, id=document_id)
    mb = ModelBuilder(doc.docfile.path, column)
    name = current_milli_time()
    pickle.dump(mb, open(settings.MEDIA_ROOT + "/pickle/" + name + ".mb", "wb"))
    response_data = {}
    response_data['model_builder'] = name
    response_data['Model_type'] = mb.model_type.name
    response_data['Available_models'] = [{
                                             "Name": name.name
                                         } for name in Selected_model]
    return JsonResponse(response_data)


def ajax_train_model(request):
    model_builder = request.GET.get('model_builder')
    model = request.GET.get('model')
    mb = pickle.load(open(settings.MEDIA_ROOT + "/pickle/" + model_builder + ".mb", "rb"))
    mb.train_model(model)
    pickle.dump(mb, open(settings.MEDIA_ROOT + "/pickle/" + model_builder + ".mb", "wb"))
    response_data = {}
    response_data['status'] = 'OK'
    response_data['model_builder'] = model_builder
    return JsonResponse(response_data)


def ajax_predict(request):
    model_builder = request.POST['model_builder']
    mb = pickle.load(open(settings.MEDIA_ROOT + "/pickle/" + model_builder + ".mb", "rb"))
    data = request.POST['data']
    data = json.loads(data)         # data = [row1, row2, ...]  row = [cell1, cell2, ...]

    # Index of column to be predicted
    column_index = int(request.POST['column_index'])

    response_data = {}
    response_data['predictions'] = mb.predict_from_data(data, column_index)
    return JsonResponse(response_data)


def ajax_upload_file(request):
    # File upload
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Add new document
            doc = Document(docfile=request.FILES['docfile'])
            doc.save()
            # Parse document, return containing data and document id
            data = get_excel_data(doc.docfile.path)
            response_data = {}
            response_data['document_id'] = doc.id
            response_data['data'] = data
            return JsonResponse(response_data)
    raise Http404("No file to upload")


def ajax_upload_predict_save(request):
    # File upload
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Add new document
            doc = Document(docfile=request.FILES['docfile'])
            doc.save()

            # Load model builder object
            model_builder = request.POST['model_builder']
            mb = pickle.load(open(settings.MEDIA_ROOT + "/pickle/" + model_builder + ".mb", "rb"))

            name = current_milli_time() + ".xls"
            mb.predict_from_file(doc.docfile.path, settings.MEDIA_ROOT + "/predictions/" + name)

            response_data = {}
            response_data['url'] = "/media/predictions/" + name
            return JsonResponse(response_data)
    raise Http404("No file to upload")


def ajax_save_to_excel(request):
    columns = request.POST['columns']
    columns = json.loads(columns)
    data = request.POST['data']
    data = json.loads(data)

    name = current_milli_time() + ".xls"
    save_to_excel(data, columns, settings.MEDIA_ROOT + "/predictions/" + name)

    response_data = {}
    response_data['url'] = '/media/predictions/' + name

    return JsonResponse(response_data)
