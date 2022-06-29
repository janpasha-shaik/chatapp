from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
# Create your models here.


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(default='192.168.190.225')
    # session_key = models.CharField(max_length=32, blank=True, null=True) 
    # picture = models.ImageField(upload_to="media/images/")

    def __str__(self):
        return self.username
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserProfile, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)