from django.urls import path, include
from .views import *

app_name='chat'

urlpatterns = [
    path('create_room/',create_room, name='create_room'),
    path('room_list/',room_list, name='room_list'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
    path('room/<int:room_id>/delete/', delete_room, name='delete_room'),
]