from django.contrib import admin

from .models import JobsList, Job, JobsFilters, WishlistJobs, ScrapedJobs

# Register your models here.
admin.site.register(JobsList)
admin.site.register(ScrapedJobs)
admin.site.register(JobsFilters)
admin.site.register(WishlistJobs)
admin.site.register(Job)
