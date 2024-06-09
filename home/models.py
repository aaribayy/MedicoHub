from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class SignUp (models.Model):
    name = models.CharField(max_length=122),
    email = models.EmailField(max_length=122),
    password = models.CharField(max_length=50),

class Register(models.Model):
    uname = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=122,unique=True)
    password = models.CharField(max_length=128)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    analysis = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.subject} by {self.user.username}"


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=500, default='')
    Precautions = models.CharField(max_length=500)
    Medications = models.CharField(max_length=500)
    workout = models.CharField(max_length=500)
    diet = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"