from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateField(auto_now=True)
    send_msg_friend = models.IntegerField(null=True, blank=True)
    receive_msg_friend = models.IntegerField(null=True, blank=True)
    
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    
class Group(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self):
        return self.name
class AddFriends(models.Model):
    request_friends = models.ForeignKey(User,on_delete=models.CASCADE,  related_name="request_friend" ,  )
    receive_friends = models.ForeignKey(User,on_delete=models.CASCADE,  related_name="receive_friend", null=True, blank=True )
    relationship = models.CharField(default=True, max_length=1000)