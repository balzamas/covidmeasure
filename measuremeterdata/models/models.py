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
    average_death_per_day = models.DecimalField(default=0,max_digits=17, decimal_places=5)
    average_death_per_day_peak = models.DecimalField(default=0,max_digits=17, decimal_places=5)
    avg_desc = models.CharField(max_length=500,blank=True,null=True)
    avg_peak_desc = models.CharField(max_length=500,blank=True,null=True)
    peak_year = models.CharField(max_length=4,blank=True,null=True)
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

class MeasureType_old(MotherModel):
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

class Measure_old(MotherModel):
    LEVEL_CHOICES=[
        (0, 'None'),
        (1, 'Partial'),
        (2, 'Full'),
    ]

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    type = models.ForeignKey(MeasureType_old, on_delete=models.CASCADE)
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
    deathstotal_average = models.DecimalField(max_digits=50, decimal_places=8, blank=True,null=True)
    deaths_past14days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    deaths_past7days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    cases_past14days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    cases_past7days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    positivity = models.DecimalField(max_digits=9, decimal_places=4,blank=True,null=True)
    development7to7 = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    r0peak = models.DecimalField(max_digits=17, decimal_places=5, null=True, blank=True)
    r0low = models.DecimalField(max_digits=17, decimal_places=5, null=True, blank=True)
    r0median = models.DecimalField(max_digits=17, decimal_places=5, null=True, blank=True)
    tests = models.IntegerField(blank=True,null=True)
    tests_smoothed_per_thousand = models.DecimalField(max_digits=17, decimal_places=5, null=True, blank=True)
    stringency_index = models.DecimalField(max_digits=17, decimal_places=5, null=True, blank=True)
    death_to_cases = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    people_vaccinated_per_hundred = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    ordering = ['country__pk', 'date', 'cases', 'deaths']

    def __str__(self):
        return f"{self.country} {self.date}"


class CountryMeasureType(MotherModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2)
    text_level0 = models.CharField(max_length=200,null=True,blank=True)
    text_level1 = models.CharField(max_length=200,null=True,blank=True)
    text_level2 = models.CharField(max_length=200,null=True,blank=True)
    text_level3 = models.CharField(max_length=200,null=True,blank=True)
    text_level4 = models.CharField(max_length=200,null=True,blank=True)
    isactive = models.BooleanField(default= True)
    ordering = ['code', 'name']
    icon =models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.name

class CountryMeasure(MotherModel):

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    type = models.ForeignKey(CountryMeasureType, on_delete=models.CASCADE)
    start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True,blank=True)
    comment = RichTextField(blank=True)
    level = models.IntegerField(default=0)
    last_level = models.IntegerField(default=0,null=True,blank=True)
    isregional = models.BooleanField(default= False)
    source = models.TextField(max_length=300,blank=True)

    ordering = ['country', 'type__code', 'type__name']

    def __str__(self):
        return f"{self.country} {self.type}"
