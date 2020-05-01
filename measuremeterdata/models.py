from django.db import models
from ckeditor.fields import RichTextField

class Continent(models.Model):
    name = models.CharField(max_length=200)
    ordering = ['name']

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3,blank=True,null=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE,blank=True,null=True)
    link_worldometer = models.CharField(max_length=200,blank=True,null=True)
    link_gov = models.CharField(max_length=200,blank=True,null=True)
    comment = RichTextField(blank=True)
    ordering = ['name']

    def __str__(self):
        return self.name

class MeasureCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class MeasureType(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(MeasureCategory, on_delete=models.CASCADE,blank=True,null=True)
    comment = RichTextField(blank=True)
    isactive = models.BooleanField(default= True)
    ordering = ['category', 'name']

    def __str__(self):
        return self.name

class Measure(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    type = models.ForeignKey(MeasureType, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(null=True,blank=True)
    partial = models.BooleanField(default=False)
    comment = RichTextField(blank=True)
    isregional = models.BooleanField(default= False)
    sources = models.TextField(max_length=300,blank=True)

    ordering = ['country', 'type']

    def __str__(self):
        return f"{self.country} {self.type}"


