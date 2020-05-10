from django.urls import path, re_path
from . import views

app_name = 'wxmessage'

urlpatterns = [
    re_path('^replytype/', views.send_message, name='send_message'),
    path('create_menu/', views.create_menu, name='create_menu'),
]
