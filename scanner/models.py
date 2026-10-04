from django.db import models
from django.conf import settings
# Create your models here.


class RobloxProject(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, #عشان استخدم الاسم الموجود
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
def __str__(self):
    return self.name



class codeScan(models.Model):
    project= models.ForeignKey(
        RobloxProject,
        on_delete=models.CASCADE,
        related_name  ="scans"

    )
    code= models.TextField()
    score=models.IntegerField(default=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
def __str__(self):
    return f"{self.project.name} -Scan{self.id}"



class securityIssue(models.Model):
    scan =models.ForeignKey(
        codeScan,
        on_delete=models.CASCADE,
        related_name="issues"
    )
    ruleID = models.CharField(max_length=10)
    title= models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    severity=models.CharField(max_length=20)
    line_number=models.IntegerField(null=True,blank= True)
    message =models.TextField()
def __str__(self):
    return f"{self.ruleID}- {self.title}"
