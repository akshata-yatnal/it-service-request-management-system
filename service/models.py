from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    class Meta:
         verbose_name_plural = "Categories"
         
    def __str__(self):
        return self.name

# python
class Ticket(models.Model):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='created_tickets')  
    
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_tickets')


    title = models.CharField(max_length=200)
    description = models.TextField()
    resolution = models.TextField(blank=True,null=True)

    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='Medium')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"

