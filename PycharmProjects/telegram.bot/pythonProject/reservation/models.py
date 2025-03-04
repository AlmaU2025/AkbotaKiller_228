from django.db import models
from django.contrib.auth.models import User
from tables.models import Table
from django.contrib.auth.models import User


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    class Reservation(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        table = models.ForeignKey(Table, on_delete=models.CASCADE)
        date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Reservation {self.id} - {self.user.username} - {self.table.number} - {self.status}"

# Create your models here.
