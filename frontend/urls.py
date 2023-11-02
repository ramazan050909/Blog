from django.urls import path

from .views import articles_list

urlpatterns = [
    path('articles/', articles_list)
]