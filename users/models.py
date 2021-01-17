from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_hr_admin = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.username)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hr_admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    is_hr_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=30)
    team = models.CharField(max_length=30)
    salary = models.FloatField()
    phone = models.CharField(max_length=30)

    def __str__(self):
        return str(self.user.username)


class FAQS(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=2000)


class Policies(models.Model):
    policy = models.CharField(max_length=2000)


class Holidays(models.Model):
    reason = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()