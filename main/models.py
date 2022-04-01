from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class UserJobs(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    sent = models.BooleanField()
    scraped = models.BooleanField()
    wishlist = models.BooleanField()
    deleted = models.BooleanField()

    def __str__(self):
        return f'{self.username} - {self.job}'


class Keyword(models.Model):
    keyword = models.CharField(max_length=50)

    def __str__(self):
        return self.keyword


class JobsFilters(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username} - {self.keyword}'


class JsonUpload(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=20)
    json_file = models.FileField(upload_to='media/')

    def __str__(self):
        return f'{self.username}-{self.file_id}'
