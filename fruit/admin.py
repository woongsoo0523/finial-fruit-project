from django.contrib import admin
from .models import FruitTable,FruitImg,FruitSugar

# Register your models here.
class Fruit(admin.TabularInline):
    model = FruitTable
    
class Fruit2(admin.TabularInline):
    model = FruitImg 
    
class Fruit3(admin.TabularInline):
    model = FruitSugar
    
admin.site.register(FruitTable)
admin.site.register(FruitImg)
admin.site.register(FruitSugar)