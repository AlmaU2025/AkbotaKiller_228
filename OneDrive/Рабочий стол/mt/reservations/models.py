from django.db import models
from django.db.models import CASCADE
from customers.models import Customer
from tables.models import Table

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    table = models.ForeignKey(Table, on_delete=CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Reservation {self.id} for {self.customer.name} on {self.date}"
