from django.urls import path, re_path
from . import views

app_name = 'wxmessage'

urlpatterns = [
    re_path('^replytype/', views.send_message, name='send_message')
]
