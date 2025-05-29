from django.db import models
from django.utils import timezone
class Profile(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    def __str__(self):
        return self.name
# Create your models here.
class New_Profile(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    resume_file=models.FileField(upload_to='uploads/resumes')
    image_file=models.ImageField(upload_to='uploads/photos')
    def __str__(self):
        return self.name
class WorkLog(models.Model):
    employee=models.ForeignKey(Profile,on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now)  
    morning_work=models.TextField(blank=True)  
    evening_work=models.TextField(blank=True)
    class Meta:
        unique_together=('employee','date')
    def __str__(self):
        return f"{self.employee.name}-{self.date}"    