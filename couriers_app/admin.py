from django.contrib import admin

from .models import Customer, Company, PackageDetail, Employee, Depot, TrackStatus

# Register your models here.
admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(PackageDetail)
admin.site.register(Employee)
admin.site.register(Depot)
admin.site.register(TrackStatus)