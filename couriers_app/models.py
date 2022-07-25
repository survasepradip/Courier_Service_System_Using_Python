from operator import truediv
import this
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10,null=False)
    zip = models.CharField(max_length=6, null=True)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=180, null=True)

    def __str__(self):
        return self.user.username

class Company(models.Model):
    company_admin = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=120, null=False)
    zip = models.CharField(max_length=6, null=False)
    address = models.CharField(max_length=180, null=False)
    contact = models.CharField(max_length=10, null=False)
    city = models.CharField(max_length=120)
    company_email = models.EmailField()

    def __str__(self):
        return self.name

class Depot(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    zip = models.CharField(max_length=6)

    def __str__(self):
        return "Depot: "+self.company.name + " - " + self.city

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    address = models.CharField(max_length=180, null=False)
    contact = models.CharField(max_length=10)
    city = models.CharField(max_length=120)
    zip = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class PackageDetail(models.Model):
    
    # sender information
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    # Reciever Information reciever identifier "r_"
    r_name = models.CharField(max_length=80, null=False)
    r_contact = models.CharField(max_length=10, null=False)
    r_address = models.CharField(max_length=180, null=False)
    r_city = models.CharField(max_length=100, null=False)
    r_zip = models.CharField(max_length=6, null=False)

    # Depot/Company and Status details
    pick_up_depot = models.ForeignKey(Depot, on_delete=models.CASCADE, null=True)
    track_no = models.IntegerField()

    pickup_datetime = models.DateTimeField(auto_now_add=True)
    drop_date = models.DateField(null=True)

    status = models.CharField(max_length=120, null=True)
    cost = models.FloatField(null=True)

    # Package Information
    pack_details = models.CharField(max_length=200, null=True)
    pack_weight = models.FloatField(null=False)

    def __str__(self):
        return "Package from " + self.sender.user.username + " to: " + self.r_name


class TrackStatus(models.Model):
    status = models.CharField(max_length=200)
    track_no = models.CharField(max_length=20)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.track_no +" "+ self.status
