from django.db import models
from django.contrib.auth.models import AbstractUser


class StUser(AbstractUser):
    USER_ROLES = (
        ('teacher', "Учитель"),
        ('student', "Студент")
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    phone_number = models.CharField(max_length=32, blank=False, null=False)
    
    def is_teacher(self):
        return self.role == "teacher"
    def is_student(self):
        return self.role == "student"
    
    def __str__(self):
        return self.username

class Teacher(models.Model):
    user = models.OneToOneField(StUser, on_delete=models.CASCADE)
    experience = models.PositiveIntegerField(default=0)
   

    def __str__(self):
        return self.user.username



    
   
