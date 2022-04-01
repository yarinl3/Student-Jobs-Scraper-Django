from django.contrib import admin
from .models import *


class UserJobsAdmin(admin.ModelAdmin):
    list_display = ("username", "job", "sent", "scraped", "wishlist", "deleted")


class JobsFiltersAdmin(admin.ModelAdmin):
    list_display = ("username", "keyword")


class JsonUploadAdmin(admin.ModelAdmin):
    list_display = ("username", "json_file")


# Register your models here.
admin.site.register(UserJobs, UserJobsAdmin)
admin.site.register(Job)
admin.site.register(JobsFilters, JobsFiltersAdmin)
admin.site.register(Keyword)
admin.site.register(JsonUpload, JsonUploadAdmin)
