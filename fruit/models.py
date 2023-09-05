from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class FruitTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    img = models.ImageField(upload_to='images/', blank=True,null=True)
    regdate = models.DateTimeField(auto_now=timezone.now)
    
class FruitImg(models.Model):
    fruittable = models.ForeignKey(FruitTable, on_delete=models.CASCADE, null=True)
    fruitresult = models.CharField(max_length=100,null=True)
    fruitresult2 = models.IntegerField(null=True)
    
class FruitSugar(models.Model):
    sugar = models.FloatField(null=True)
    fruittable = models.ForeignKey(FruitTable, on_delete=models.CASCADE, null=True)


    
