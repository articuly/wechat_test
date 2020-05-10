from django.urls import path
from . import views

app_name='authwx'

urlpatterns=[
    path('', views.auth, name='auth')
]