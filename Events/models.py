from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200) 
    description = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200) 
    description = models.TextField() 
    date = models.DateField() 
    time = models.TimeField() 
    location = models.CharField(max_length=250) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')


    def __str__(self):
        return self.name 
    
class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True) 
    Events = models.ManyToManyField(Event, related_name = "participants", blank=True)

    def __str__(self):
        return self.name