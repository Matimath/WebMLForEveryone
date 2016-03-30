from django.db import models

# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


# Pierwsza linia w Pythonie :D
class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    hash = models.CharField(max_length=20)
    upload = models.FileField(upload_to='uploads/user_files/%Y/%m/%d/')

class MLobject(models.Model):
    object_id = models.AutoField(primary_key=True)
    upload = models.FileField(upload_to='uploads/ML_object/%Y/%m/%d/')
