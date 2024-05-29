from django.db import models

# Create your models here.
class Hist(models.Model):
    text=models.TextField(max_length=500)
    label=models.CharField(max_length=10)
    prob=models.CharField(max_length=10)