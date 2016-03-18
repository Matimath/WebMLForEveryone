from django import forms

class UploadDocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )