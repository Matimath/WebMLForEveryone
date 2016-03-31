from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from upload.models import Document
from upload.forms import UploadDocumentForm

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
            return HttpResponseRedirect(reverse('choose'))
    else:
        form = UploadDocumentForm()

    # All uploaded documents
    docs = Document.objects.all()

    # Render page using model parameters
    return render(request, 'upload.html', {
        'docs': docs,
        'form': form
    })

def _upload(request):
    return render(request, 'upload.html')

def choose(request):
    return render(request, 'choose.html')

def compute(request):
    return render(request, 'compute.html')
