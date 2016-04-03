from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import UserFile
from .models import MachineLearningObject

admin.site.register(UserFile)

admin.site.register(MachineLearningObject)