from django.urls import path, include
from .views import*

app_name='users'

urlpatterns = [
    path('signup/',signup, name='signup'),
    path('',signin, name='signin'),
    path('signout/',signout, name='signout'),
  
]