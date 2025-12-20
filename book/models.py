from django.db import models
from django.utils import timezone
from datetime import time
# Create your models here.

#profile of the user 
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, db_index=True)
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return f"{self.user} - {self.currency}"

#model that stores task
class Task(models.Model):
    user =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    start = models.TimeField(default=time(0, 0))  
    end = models.TimeField(default=time(0, 0))
    job_name = models.CharField(max_length=50, default="N/A")
    class Meta: #for better queries
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.start}| {self.end} | {self.job_name}"