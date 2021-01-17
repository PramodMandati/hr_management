from django.db import models
from users.models import Employee


# Create your models here.
class LeaveModel(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    start_date = models.DateField()
    end_date = models.DateField()
    is_approve = models.NullBooleanField()

    class Meta:
        ordering = ('-id',)
