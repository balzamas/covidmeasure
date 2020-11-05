from django.db import models
from ckeditor.fields import RichTextField

class MotherModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Continent(MotherModel):
    name = models.CharField(max_length=200)
    ordering = ['name']

    def __str__(self):
        return self.name

class Country(MotherModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3,blank=True,null=True)
    iso_code = models.CharField(max_length=3,blank=True,null=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE,blank=True,null=True)
    link_worldometer = models.CharField(max_length=200,blank=True,null=True)
    link_gov = models.CharField(max_length=200,blank=True,null=True)
    link_dashboard = models.CharField(max_length=200,blank=True,null=True)
    comment = RichTextField(blank=True)
    isactive = models.BooleanField(default= True)
    average_death_per_day = models.DecimalField(default=0,max_digits=7, decimal_places=1)
    average_death_per_day_peak = models.DecimalField(default=0,max_digits=7, decimal_places=1)
    avg_desc = models.CharField(max_length=500,blank=True,null=True)
    avg_peak_desc = models.CharField(max_length=500,blank=True,null=True)
    source_death = models.CharField(max_length=500,blank=True,null=True)
    population = models.IntegerField(default=1)
    has_measures = models.BooleanField(default= True)

    ordering = ['name']

    def __str__(self):
        return self.name

class MeasureCategory(MotherModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class MeasureType(MotherModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(MeasureCategory, on_delete=models.CASCADE,blank=True,null=True)
    comment = RichTextField(blank=True)
    tooltip_nonpartial =models.CharField(max_length=200,blank=True)
    tooltip_partial =models.CharField(max_length=200,blank=True)
    isactive = models.BooleanField(default= True)
    ordering = ['category', 'name']
    icon =models.CharField(max_length=200,blank=True)


    def __str__(self):
        return self.name

class Measure(MotherModel):
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


class CasesDeaths(MotherModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date = models.DateField()
    cases = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    deathstotal = models.DecimalField(max_digits=50, decimal_places=8, blank=True,null=True)
    deathstotal_peak = models.DecimalField(max_digits=50, decimal_places=8, blank=True,null=True)
    deaths_per100k = models.DecimalField(max_digits=9, decimal_places=4,blank=True,null=True)
    deaths_total_per100k = models.DecimalField(max_digits=9, decimal_places=4,blank=True,null=True)
    deaths_past14days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    cases_per_mio = models.DecimalField(max_digits=9, decimal_places=2,blank=True,null=True)
    cases_per_mio_seven = models.DecimalField(max_digits=9, decimal_places=2,blank=True,null=True)
    cases_past14days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    cases_past7days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    positivity = models.DecimalField(max_digits=9, decimal_places=4,blank=True,null=True)
    development7to7 = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)

    ordering = ['country__pk', 'date', 'cases', 'deaths']

    def __str__(self):
        return f"{self.country} {self.date}"


