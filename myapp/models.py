from django.db import models

# Create your models here
class courseconcept(models.Model):
    courseconcept=models.CharField(max_length=30)
    
    def __str__(self):
        return self.courseconcept


class coursemodel(models.Model):
    coursename = models.CharField(max_length=100)
    courseimage = models.ImageField()
    description = models.CharField(max_length=200)
    courselist= models.ManyToManyField(courseconcept)
    courseprice=models.IntegerField()
    courseTutor=models.CharField(max_length=30)

    def __str__(self):
        return self.coursename