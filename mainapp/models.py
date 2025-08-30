from django.db import models


class Enquiry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    enquirydate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}->{self.phone}"


# Create your models here.
class LoginInfo(models.Model):
    usertype = models.CharField(max_length=10)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=256)
    status = models.CharField(max_length=10, default="active")

    def __str__(self):
        return f"{self.username}->{self.usertype}"


class UserInfo(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(max_length=15)
    address = models.TextField()
    profile = models.ImageField(upload_to="profiles/", blank=True, null=True)
    login = models.OneToOneField(LoginInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
