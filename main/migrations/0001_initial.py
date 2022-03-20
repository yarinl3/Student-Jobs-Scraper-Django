# Generated by Django 4.0.3 on 2022-03-20 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='JobsFilters',
            fields=[
                ('jobs_list', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.jobslist')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapedJobs',
            fields=[
                ('jobs_list', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.jobslist')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WishlistJobs',
            fields=[
                ('jobs_list', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.jobslist')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=50)),
                ('jobs_filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.jobsfilters')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('link', models.CharField(max_length=300)),
                ('sent', models.BooleanField()),
                ('scraped_jobs', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.scrapedjobs')),
                ('wishlist_jobs', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.wishlistjobs')),
            ],
        ),
    ]