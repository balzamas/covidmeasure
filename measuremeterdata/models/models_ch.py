from django.db import models
from ckeditor.fields import RichTextField

class MotherModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CHCanton(MotherModel):
    LEVEL_CHOICES=[
        (0, 'Canton'),
        (1, 'Disctrict'),
        (2, 'Commune'),
        (3, 'Federation'),
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
    comment_orig = RichTextField(blank=True)
    sources = models.TextField(max_length=900,blank=True)
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
    development7to7 = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)


    ordering = ['canton__pk', 'date', 'cases']

    def __str__(self):
        return f"{self.canton} {self.date}"
