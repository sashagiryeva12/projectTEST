from django.db import models
from users.models import StUser

class Room(models.Model):
    name = models.CharField(max_length=100)

    teacher = models.ForeignKey(
        StUser,
        on_delete=models.CASCADE,
        related_name='created_rooms' 
    )

    members = models.ManyToManyField(
        StUser,
        related_name='rooms'        
    )



class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(StUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

