from django.db import models


# Create your models here.
class JobsList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ScrapedJobs(models.Model):
    jobs_list = models.OneToOneField(JobsList, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class JobsFilters(models.Model):
    scraped_jobs = models.ForeignKey(ScrapedJobs, on_delete=models.CASCADE)
    keyword_filter = models.CharField(max_length=50)

    def __str__(self):
        return self.keyword_filter


class WishlistJobs(models.Model):
    jobs_list = models.OneToOneField(JobsList, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Job(models.Model):
    scraped_jobs = models.ForeignKey(ScrapedJobs, on_delete=models.CASCADE, null=True)
    wishlist_jobs = models.ForeignKey(WishlistJobs, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=300)
    sent = models.BooleanField()

    def __str__(self):
        return self.title
