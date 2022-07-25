from dataclasses import field, fields
from pyexpat import model
from turtle import textinput
from django import forms
from django.contrib.auth.models import User
from .models import Customer, Employee, Company, TrackStatus, PackageDetail, Depot

class DateInput(forms.DateInput):
    input_type = 'date'


class CustomerRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'required': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password')

    def clean(self):

        username = self.data['username']
        user = User.objects.filter(username=username)
        email = self.data['email']
        user_email = User.objects.filter(email=email)
        if user_email:
            raise forms.ValidationError({
                "email": "This email address is used already"
            })
        if user:
            raise forms.ValidationError({
                "username": "A user with this username already exists."
            })

        if self.data['password'] != self.data['password_confirm']:
            raise forms.ValidationError(
                {
                    "password": "Password and Confirm Password does not match",
                }
            )
        elif len(self.data['password']) < 8:
            raise forms.ValidationError(
                {
                    "password": "Password too short, it should be atleast 8 character long",
                }
            )


class CustomerProfForm(forms.ModelForm):

    contact = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max_length': 10}))
    zip = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max_length': 6}))
    city = forms.CharField(widget=forms.TextInput(attrs={'max_length': 120}))
    address = forms.CharField(widget=forms.TextInput(attrs={'max_length': 180}))

    class Meta:
        model = Customer
        fields = ('contact', 'zip','city','address')


class CustLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CreatePackageForm(forms.Form):

    r_name = forms.CharField(widget=forms.TextInput(attrs={'max_length' : 120}))
    r_contact = forms.CharField(widget=forms.NumberInput(attrs={'max_length' : 10}))
    r_address = forms.CharField(widget=forms.TextInput(attrs={'max_length' : 120}))
    r_city = forms.CharField(widget=forms.TextInput(attrs={'max_length' : 60}))
    r_zip = forms.CharField(widget=forms.NumberInput(attrs={'max_length' : 6}))
    pack_details = forms.CharField(widget=forms.TextInput(attrs={'max_length' : 120}))
    pack_weight = forms.FloatField()

    class Meta:
        model = PackageDetail
        fields = ('r_name', 'r_contact', 'r_address', 'r_city', 'r_zip', 'pack_details', 'pack_weight')


class CompanyCreateForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={'max_length': 120}))
    address = forms.CharField(widget=forms.TextInput(attrs={'max_length': 180}))
    zip = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max_length': 6}))
    contact = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max_length': 10}))
    
    city = forms.CharField(widget=forms.TextInput(attrs={'max_length': 120}))
    
    company_email = forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = Company
        fields = ('name', 'address','zip', 'contact', 'city', 'company_email')


class CompanyCreateDepot(forms.Form):

    contact = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max_length': 10}))
    zip = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max_length': 6}))
    city = forms.CharField(widget=forms.TextInput(attrs={'max_length': 120}))
    address = forms.CharField(widget=forms.TextInput(attrs={'max_length': 180}))

    class Meta:
        model = Depot
        fields = ('contact', 'address', 'city', 'zip')

