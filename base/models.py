from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    CHOICE = (
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=CHOICE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', 'start_time']