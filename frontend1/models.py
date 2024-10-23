from django.db import models
from django.contrib.auth.models import AbstractUser

from myapp.models import coursemodel
# Create your models here.


class CustomUser(AbstractUser):

    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email
    
class add_to_cart(models.Model):
    userid = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    courseid = models.ForeignKey(coursemodel, on_delete = models.CASCADE)

class enrolled_courses(models.Model):
    userid = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    courseid = models.ForeignKey(coursemodel, on_delete = models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)




