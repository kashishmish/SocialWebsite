from django.db import models
from datetime import datetime

class Registration(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100,unique=True,primary_key=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    img=models.ImageField(upload_to='pics')
class Addpost(models.Model):
    username=models.CharField(max_length=100)
    email=models.ForeignKey(Registration,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    img=models.ImageField(upload_to='post')
    datetime=models.DateTimeField(default=datetime.now,blank=True)
    like= models.IntegerField()
    dislike= models.IntegerField()
class Reaction(models.Model):
    post_id=models.ForeignKey(Addpost,on_delete=models.CASCADE)
    email_like=models.CharField(max_length=100)
    email_dislike=models.CharField(max_length=100)
class Friend_request(models.Model):
    email_reciever=models.CharField(max_length=100)
    email_sender=models.ForeignKey(Registration,on_delete=models.CASCADE)
    confirmation=models.IntegerField()
class Comments(models.Model):
    email=models.ForeignKey(Registration,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Addpost,on_delete=models.CASCADE)
    datetime=models.DateTimeField(default=datetime.now,blank=True)
    message=models.CharField(max_length=500)