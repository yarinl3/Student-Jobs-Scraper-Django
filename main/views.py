from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from mysite.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from .forms import *
from .Student_Jobs import jobs_scrape
from .models import *
from threading import Thread
import random
import time
import boto3
from boto3.session import Session
# Do not delete this imports.
# These imports for requirements.txt
import storages
import gunicorn

CHECKBOX_LIST = ["alljobs", "drushim", "jobmaster", "sqlink", "telegram_jobs", "jobnet", "indeed"]  # noqa
TIMEOUT = 25


# Create your views here.
def home(response):
    form = GuestRegistrationForm()
    if response.user.is_anonymous is True:
        if response.method == "POST":
            form = GuestRegistrationForm(response.POST)
            if form.is_valid():
                val = form.cleaned_data.get("btn")
                if val == 'לחץ כאן':
                    try:
                        while True:
                            username = f'guest-{random.randint(1,100000)}'
                            if len(User.objects.filter(username=username)) == 0:
                                user = User.objects.create_user(username=username, password='12345')
                                user.is_superuser = False
                                user.is_staff = False
                                user.save()
                                break

                        user = User.objects.get(username=username)
                        guest1_filter = User.objects.filter(username='guest-1')
                        guest1 = guest1_filter[0] if len(guest1_filter) > 0 else None
                        if guest1 is not None:
                            for job in Job.objects.all():
                                if len(job.userjobs_set.filter(username=guest1)) != 0:
                                    guest1_userjob = job.userjobs_set.get(username=guest1)
                                    job.userjobs_set.create(username=user,
                                                            sent=guest1_userjob.sent,
                                                            scraped=guest1_userjob.scraped,
                                                            wishlist=guest1_userjob.wishlist,
                                                            deleted=guest1_userjob.deleted)

                            for keyword in Keyword.objects.all():
                                if len(keyword.jobsfilters_set.filter(username=guest1)) != 0:
                                    guest1_jobfilters = keyword.jobsfilters_set.get(username=guest1)
                                    keyword.jobsfilters_set.create(username=user, keyword=guest1_jobfilters.keyword)

                    except Exception as e:
                        print(f'Error in views.home, username = {username}, Error: {e}')

                    finally:
                        if user is not None:
                            login(response, user)
                            return redirect('/scraped_list')
    else:
        return redirect('/scraped_list')
    return render(response, 'main/home.html', {'form': form, 'username': response.user})


def same_code(response, page_name):
    if response.user.is_anonymous is False:
        user = response.user
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                user_job = Job.objects.filter(link=link)[0].userjobs_set.filter(username=user)
                if val == 'Delete':
                    user_job.update(sent=False, scraped=False, wishlist=False, deleted=True)
                if page_name == 'scraped_list':
                    if val == 'Add to Wishlist':
                        user_job.update(sent=False, scraped=False, wishlist=True, deleted=False)
                if page_name in ['scraped_list', 'wishlist']:
                    if val == 'Add to Sent':
                        user_job.update(sent=True, scraped=False, wishlist=False, deleted=False)
        else:
            form = JobsListFrom()
        new_jobs = []
        jobs = Job.objects.all()
        for job in jobs:
            if len(job.userjobs_set.filter(username=user, sent=(page_name == 'sent'),
                                           scraped=(page_name == 'scraped_list'), wishlist=(page_name == 'wishlist'),
                                           deleted=False)) != 0:
                new_jobs.append(job)
        return render(response, f'main/{page_name}.html', {'form': form, 'jobs': new_jobs, 'username': user})
    else:
        raise PermissionDenied()


def scraped_list(response):
    return same_code(response, 'scraped_list')


def wishlist(response):
    return same_code(response, 'wishlist')


def sent(response):
    return same_code(response, 'sent')


def pre_scrape(response):
    global TIMEOUT
    scrape_start_time = time.time()
    if response.user.is_anonymous is False:
        errors = []
        threads = []
        user = response.user
        form = ScrapeForm()
        if response.method == "POST":
            form = ScrapeForm(response.POST)
            if 'save' in response.POST:
                if form.is_valid():
                    res = response.POST
                    checked_list = [key for key in res if key in CHECKBOX_LIST and res.get(key) == 'on']

                    def scrape(checkbox):
                        if checkbox == 'telegram_jobs' and 'upload_json' in response.FILES:
                            num = upload_s3_file(user, response.FILES['upload_json'])
                            if num is not None:
                                s3_file = get_s3_file(user, num)
                            else:
                                errors.append(f'Failed to scrape {checkbox}.\nOnly json files can be uploaded.')
                            error_flag, error_value = jobs_scrape(checkbox, user, s3_file)
                        else:
                            error_flag, error_value = jobs_scrape(checkbox, user)

                        if error_flag is True:
                            errors.append(f'{checkbox} scraped successfully.')
                        else:
                            errors.append(error_value)
                    for checked in checked_list:
                        t = Thread(target=scrape, args=(checked,))
                        threads.append(t)
                        t.start()
                    for t in threads:
                        start_time = time.time()
                        t.join(TIMEOUT)
                        TIMEOUT -= time.time() - start_time
                        if TIMEOUT < 0:
                            TIMEOUT = 0
                    errors = collect_errors(checked_list, errors, scrape_start_time)
            elif 'reset' in response.POST:
                user_job = UserJobs.objects.filter(username=user, deleted=True)
                user_job.update(sent=False, scraped=True, wishlist=False, deleted=False)
        return render(response, 'main/scrape.html', {'form': form, 'errors': errors, 'username': user,
                                                     'sites': CHECKBOX_LIST})
    else:
        raise PermissionDenied()


def keywords(response):
    if response.user.is_anonymous is False:
        user = response.user
        add_form = AddKeywordForm(response.POST)
        del_form = DeleteKeywordForm(response.POST)
        update_form = UpdateKeywordForm(response.POST)
        keywords_list = set([str(i.keyword) for i in JobsFilters.objects.filter(username=user)])
        if response.method == "POST":
            if add_form.is_valid():
                keyword = add_form.cleaned_data.get('keyword').lower()
                if keyword != '' and keyword.isspace() is False:
                    keyword_exist = len(Keyword.objects.all().filter(keyword=keyword)) != 0
                    if keyword_exist is True:
                        old_keyword = Keyword.objects.filter(keyword=keyword)[0]
                        keyword_exist_in_others = len(old_keyword.jobsfilters_set.filter(username=user)) == 0
                        if keyword_exist_in_others is True:
                            old_keyword.jobsfilters_set.create(username=user)
                    else:
                        new_keyword = Keyword(keyword=keyword)
                        new_keyword.save()
                        new_keyword.jobsfilters_set.create(username=user)

            elif del_form.is_valid():
                keyword = del_form.cleaned_data.get('delete').lower()
                Keyword.objects.filter(keyword=keyword)[0].jobsfilters_set.filter(username=user).delete()
            elif update_form.is_valid():
                jobs_id = []
                userjobs = UserJobs.objects.filter(username=user, scraped=True)
                checkbox = update_form.cleaned_data.get("ckbx")
                for userjob in userjobs:
                    job = Job.objects.filter(id=userjob.job_id)[0]
                    link = job.link.lower()
                    words = job.title.lower().split(' ')
                    flag = False
                    for word in words:
                        if word in keywords_list:
                            flag = True
                            break
                    if checkbox is True:
                        for keyword in keywords_list:
                            if keyword in link:
                                flag = True
                                break
                    if flag is True:
                        jobs_id.append(job.id)

                UserJobs.objects.filter(username=user, job_id__in=jobs_id).update(sent=False,
                                                                                  scraped=False,
                                                                                  wishlist=False,
                                                                                  deleted=True)
        keywords_list = set([str(i.keyword) for i in JobsFilters.objects.filter(username=user)])
        return render(response, 'main/keywords.html', {'form': add_form, 'keywords': keywords_list,
                                                       'username': user})
    else:
        raise PermissionDenied()


def collect_errors(checked_list, errors, scrape_start_time):
    for site in checked_list:
        site_in_errors = False
        for error in errors:
            if site in str(error):
                site_in_errors = True
        if site_in_errors is False and time.time() - scrape_start_time >= 25:
            errors.append(f'Timeout: 25 seconds passed and the scraping did not end.\n'
                          f'If the connection to {site} is correct it will continue the scraping'
                          f' in the background. ')
    return errors


def upload_s3_file(user, file):
    num_list = sorted([int(file_obj.file_id) for file_obj in JsonUpload.objects.filter(username=user)])
    try:
        num = num_list[-1] + 1
    except IndexError:
        num = 1
    if file.name.endswith('.json') is True:
        file.name = f"{user}-{num}.json"
        JsonUpload.objects.create(username=user, file_id=num, json_file=file)
        return num


def get_s3_file(user, num):
    session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    s3_file = s3.Object(AWS_STORAGE_BUCKET_NAME, f'media/{user}-{num}.json').get()['Body']
    return s3_file
