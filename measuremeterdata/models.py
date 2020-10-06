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
    deathstotal = models.IntegerField(default=0)
    deaths_per100k = models.DecimalField(max_digits=9, decimal_places=4,blank=True,null=True)
    deaths_total_per100k = models.DecimalField(max_digits=9, decimal_places=4,blank=True,null=True)
    deaths_past14days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    cases_per_mio = models.DecimalField(max_digits=9, decimal_places=2,blank=True,null=True)
    cases_per_mio_seven = models.DecimalField(max_digits=9, decimal_places=2,blank=True,null=True)
    cases_past14days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    cases_past7days = models.DecimalField(max_digits=50, decimal_places=2,blank=True,null=True)
    positivity = models.DecimalField(max_digits=9, decimal_places=4,blank=True,null=True)

    ordering = ['country__pk', 'date', 'cases', 'deaths']

    def __str__(self):
        return f"{self.country} {self.date}"

class CHCanton(MotherModel):
    LEVEL_CHOICES=[
        (0, 'Canton'),
        (1, 'Disctrict'),
        (2, 'Commune'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3,blank=True,null=True)
    population = models.IntegerField(default=1)
    swisstopo_id = models.CharField(max_length=200)
    level = models.IntegerField(choices=LEVEL_CHOICES,default=0)

    ordering = ['name']

    def __str__(self):
        return self.name

class CHMeasureType(MotherModel):
    name = models.CharField(max_length=200)
    comment = RichTextField(blank=True)
    tooltip_level1 =models.CharField(max_length=200,blank=True)
    tooltip_level2 =models.CharField(max_length=200,blank=True)
    tooltip_level3 =models.CharField(max_length=200,blank=True)
    tooltip_level4 =models.CharField(max_length=200,blank=True)
    isactive = models.BooleanField(default= True)
    ordering = ['name']
    icon =models.CharField(max_length=200,blank=True)


    def __str__(self):
        return self.name

class CHMeasure(MotherModel):
    LEVEL_CHOICES=[
        (0, 'Level 1'),
        (1, 'Level 2'),
        (2, 'Level 3'),
        (3, 'Level 4'),
    ]

    canton = models.ForeignKey(CHCanton, on_delete=models.CASCADE)
    type = models.ForeignKey(CHMeasureType, on_delete=models.CASCADE)
    start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True,blank=True)
    level = models.IntegerField(choices=LEVEL_CHOICES,default=0)
    comment = RichTextField(blank=True)
    sources = models.TextField(max_length=300,blank=True)
    isregional = models.BooleanField(default= False)

    ordering = ['canton', 'type__category', 'type__name']

    def __str__(self):
        return f"{self.canton} {self.type}"


class CHCases(MotherModel):
    canton = models.ForeignKey(CHCanton, on_delete=models.CASCADE)
    date = models.DateField()
    cases = models.IntegerField(null=True,blank=True)
    incidence_past14days = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    incidence_past10days = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    incidence_past7days = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)

    ordering = ['canton__pk', 'date', 'cases']

    def __str__(self):
        return f"{self.canton} {self.date}"

class BELProvince(MotherModel):
    name = models.CharField(max_length=200)
    name_source = models.CharField(max_length=200,blank=True,null=True)
    population = models.IntegerField(default=1)

    ordering = ['name']

    def __str__(self):
        return self.name

class BELAgeGroups(MotherModel):
    name = models.CharField(max_length=200)
    population = models.IntegerField(default=1)
    ordering = ['name']

    def __str__(self):
        return self.name

class BELCases(MotherModel):
    province = models.ForeignKey(BELProvince, on_delete=models.CASCADE)
    date = models.DateField()
    cases0_9 = models.IntegerField(default=0)
    cases10_19 = models.IntegerField(default=0)
    cases20_29 = models.IntegerField(default=0)
    cases30_39 = models.IntegerField(default=0)
    cases40_49 = models.IntegerField(default=0)
    cases50_59 = models.IntegerField(default=0)
    cases60_69 = models.IntegerField(default=0)
    cases70_79 = models.IntegerField(default=0)
    cases80_89 = models.IntegerField(default=0)
    cases90plus = models.IntegerField(default=0)
    ordering = ['province__pk', 'date', 'cases']

    def __str__(self):
        return f"{self.province} {self.date}"
