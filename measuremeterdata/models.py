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
    mapcode_europe = models.CharField(max_length=10,blank=True,null=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE,blank=True,null=True)
    link_worldometer = models.CharField(max_length=200,blank=True,null=True)
    link_gov = models.CharField(max_length=200,blank=True,null=True)
    comment = RichTextField(blank=True)
    isactive = models.BooleanField(default= True)
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
    tooltip_nonpartial =models.CharField(max_length=200,blank=True)
    tooltip_partial =models.CharField(max_length=200,blank=True)
    isactive = models.BooleanField(default= True)
    ordering = ['category', 'name']

    def __str__(self):
        return self.name

class Measure(models.Model):
    LEVEL_CHOICES=[
        (0, 'None'),
        (1, 'Partial'),
        (2, 'Full'),
    ]

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    type = models.ForeignKey(MeasureType, on_delete=models.CASCADE)
    start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True,blank=True)
    level = models.IntegerField(choices=LEVEL_CHOICES,default=0)
    comment = RichTextField(blank=True)
    isregional = models.BooleanField(default= False)
    sources = models.TextField(max_length=300,blank=True)

    ordering = ['country', 'type__category', 'type__name']

    def __str__(self):
        return f"{self.country} {self.type}"


class CasesDeaths(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date = models.DateField()
    cases = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)

    ordering = ['country__pk', 'date', 'cases', 'deaths']

    def __str__(self):
        return f"{self.country} {self.date}"
