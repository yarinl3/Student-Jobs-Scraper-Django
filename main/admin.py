from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserJobs)
admin.site.register(Job)
admin.site.register(JobsFilters)
admin.site.register(Keyword)
admin.site.register(JsonUpload)

