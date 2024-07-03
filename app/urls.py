from django.urls import path
from . import views

urlpatterns = [
    path('file/', views.FileList.as_view(), name='file-list')
]