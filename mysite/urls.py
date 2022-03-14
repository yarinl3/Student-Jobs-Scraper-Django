from django.contrib import admin
from django.urls import path, include, re_path
from register import views as v
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', v.register, name='register'),
    path('', include("main.urls")),
    path('', include("django.contrib.auth.urls")),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
]
