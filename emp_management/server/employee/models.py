from django.db import models
from basics.models import Technology
from const import GENDER
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee")
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER, default="Male")
    technologies_familiar_with = models.ManyToManyField(Technology)
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


class EmployeeAttendence(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="emp_attendence"
    )
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ["date", "employee"]

    def __str__(self):
        return "{},{}".format(self.employee, self.date)
