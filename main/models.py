from django.db import models


# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class UserJobs(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    sent = models.BooleanField()
    scraped = models.BooleanField()
    wishlist = models.BooleanField()
    deleted = models.BooleanField()

    def __str__(self):
        return self.username


class Keyword(models.Model):
    keyword = models.CharField(max_length=50)

    def __str__(self):
        return self.keyword


class JobsFilters(models.Model):
    username = models.CharField(max_length=200)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    def __str__(self):
        return self.username



